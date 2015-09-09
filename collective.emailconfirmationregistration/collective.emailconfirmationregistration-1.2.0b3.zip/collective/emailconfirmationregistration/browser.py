from Products.Five import BrowserView
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from hashlib import sha1
from plone.app.users.browser.register import RegistrationForm as BaseRegistrationForm
from plone.app.discussion.browser.validator import CaptchaValidator
from plone.app.discussion.interfaces import ICaptcha
from plone.app.discussion.interfaces import IDiscussionSettings

from plone.app.users.schema import checkEmailAddress
from plone.registry.interfaces import IRegistry

from time import time
from zope import schema

from zope.component import getUtility
from zope.component import adapts
from zope.component import queryUtility

from zope.interface import Interface

from z3c.form import form
from z3c.form import button

from BTrees.OOBTree import OOBTree
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from plone.z3cform.fieldsets import extensible
from z3c.form import interfaces
from collective.emailconfirmationregistration.interfaces import ILayer
from z3c.form.field import Fields
from zope.event import notify
from z3c.form.action import ActionErrorOccurred
from z3c.form.interfaces import WidgetActionExecutionError
from zope.interface import Invalid
from plone.autoform.form import AutoExtensibleForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform.fieldsets.utils import move

import random
try:
    random = random.SystemRandom()
except NotImplementedError:
    pass


def makeRandomCode(length=255):
    return sha1(sha1(str(
        random.random())).hexdigest()[:5] + str(
        datetime.now().microsecond)).hexdigest()[:length]


class NonExistentException(Exception):
    """Dummy exception for usage instead of exceptions from missing plugins.
    """

try:
    from plone.app.discussion.browser.validator import WrongNorobotsAnswer
except ImportError:
    WrongNorobotsAnswer = NonExistentException

try:
    from plone.app.discussion.browser.validator import WrongCaptchaCode
except ImportError:
    WrongCaptchaCode = NonExistentException


def shouldBeEmpty(value):
    if value:
        raise Invalid(_(u"This should not have a value"))


class RegistrationStorage(object):

    attr_name = '_registration_confirmations'

    def __init__(self, context):
        self.context = context
        try:
            self._data = getattr(context, self.attr_name)
        except AttributeError:
            self._data = OOBTree()
            setattr(context, self.attr_name, self._data)

    def add(self, email, data=None):
        self.clean()
        email = email.lower()
        if data is None:
            data = {}
        data.update({
            'created': time(),
            'code': makeRandomCode(100)
        })
        self._data[email] = data
        return data

    def remove(self, email):
        if email.lower() in self._data:
            del self._data[email.lower()]

    def get(self, email):
        return self._data.get(email.lower())

    def clean(self):
        now = time()
        delete = []
        for email, item in self._data.items():
            if not item:
                delete.append(email)
                continue
            created = item['created']
            # delete all older than 1 hour
            if int((now - created) / 60 / 60) > 1:
                delete.append(email)
        for code in delete:
            del self._data[code]


class RegistrationReviewStorage(RegistrationStorage):
    attr_name = '_registrations_under_review'


class IEmailConfirmation(ICaptcha):
    email = schema.ASCIILine(
        title=_(u'label_email', default=u'E-mail'),
        description=u'',
        required=True,
        constraint=checkEmailAddress)
    username = schema.ASCIILine(
        required=False,
        constraint=shouldBeEmpty)


class EmailConfirmation(AutoExtensibleForm, form.Form):
    label = u"Confirm your email address"
    description = (u"Before you can begin the registration process, you need to "
                   u"verify your email address.")
    formErrorsMessage = _('There were errors.')
    ignoreContext = True
    schema = IEmailConfirmation
    enableCSRFProtection = True
    template = ViewPageTemplateFile('confirm-email.pt')
    sent = False

    def __init__(self, context, request):
        super(EmailConfirmation, self).__init__(context, request)
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        self.captcha = settings.captcha
        portal_membership = getToolByName(self.context, 'portal_membership')
        self.isAnon = portal_membership.isAnonymousUser()

    def send_mail(self, email, item):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Email Confirmation"
        msg['From'] = getUtility(ISiteRoot).email_from_address
        msg['To'] = email
        url = '%s/@@register?confirmed_email=%s&confirmed_code=%s' % (
            self.context.absolute_url(), email, item['code'])
        text = """
Copy and paste this url into your web browser to confirm your address: %s
""" % url
        html = """
<p>You have requested registration, please
<a href="%s">confirm your email address by clicking on this link</a>.
</p>
<p>
If that does not work, copy and paste this urls into your web browser: %s
</p>""" % (url, url)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        mailhost = getToolByName(self.context, 'MailHost')
        mailhost.send(msg.as_string())

    def updateFields(self):
        super(EmailConfirmation, self).updateFields()
        if self.captcha != 'disabled' and self.isAnon:
            # Add a captcha field if captcha is enabled in the registry
            if self.captcha == 'captcha':
                from plone.formwidget.captcha import CaptchaFieldWidget
                self.fields['captcha'].widgetFactory = CaptchaFieldWidget
            elif self.captcha == 'recaptcha':
                from plone.formwidget.recaptcha import ReCaptchaFieldWidget
                self.fields['captcha'].widgetFactory = ReCaptchaFieldWidget
            elif self.captcha == 'norobots':
                from collective.z3cform.norobots import NorobotsFieldWidget
                self.fields['captcha'].widgetFactory = NorobotsFieldWidget
            else:
                self.fields['captcha'].mode = interfaces.HIDDEN_MODE
        else:
            self.fields['captcha'].mode = interfaces.HIDDEN_MODE

        move(self, 'email', before='*')

    def updateWidgets(self):
        super(EmailConfirmation, self).updateWidgets()
        # the username field here is ONLY for honey pot.
        # if a value IS present, throw an error
        self.widgets['username'].addClass('hiddenStructure')

    @button.buttonAndHandler(
        _(u'label_verify', default=u'Verify'), name='verify'
    )
    def action_verify(self, action):
        data, errors = self.extractData()
        if not errors:
            storage = RegistrationStorage(self.context)
            item = storage.add(data['email'])
            self.send_mail(data['email'], item)
            self.sent = True
            IStatusMessage(self.request).addStatusMessage(
                'Verification email has been sent to your email.', type='info')


class RegistrationForm(BaseRegistrationForm):

    def get_confirmed_email(self):
        req = self.request
        return req.form.get('confirmed_email', req.form.get('form.widgets.confirmed_email', ''))

    def get_confirmed_code(self):
        req = self.request
        return req.form.get(
            'confirmed_code', req.form.get('form.widgets.confirmed_code', ''))

    def verify(self):
        email = self.get_confirmed_email()
        code = self.get_confirmed_code()
        if not email or not code:
            return False
        storage = RegistrationStorage(self.context)
        entry = storage.get(email)
        if entry is None:
            return False
        if entry['code'] == code:
            return True
        return False

    def updateWidgets(self):
        super(RegistrationForm, self).updateWidgets()
        self.widgets['confirmed_email'].value = self.get_confirmed_email()
        self.widgets['confirmed_code'].value = self.get_confirmed_code()

    def validate_registration(self, action, data):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        portal_membership = getToolByName(self.context, 'portal_membership')
        captcha_enabled = settings.captcha != 'disabled'
        anon = portal_membership.isAnonymousUser()
        if captcha_enabled and anon:
            if 'captcha' not in data:
                data['captcha'] = u""
            try:
                captcha = CaptchaValidator(self.context,
                                           self.request,
                                           None,
                                           ICaptcha['captcha'],
                                           None)
                captcha.validate(data['captcha'])
            except (WrongCaptchaCode, WrongNorobotsAnswer):
                # Error messages are fed in by the captcha widget itself.
                pass

        if 'captcha' in data:
            del data['captcha']  # delete, so that value isn't stored

        super(RegistrationForm, self).validate_registration(action, data)

        if 'email' in data and data['email'].lower() != self.get_confirmed_email().lower():
            err_str = u'Email address you have entered does not match email used in verification'
            notify(
                ActionErrorOccurred(
                    action, WidgetActionExecutionError('email', Invalid(err_str))
                )
            )
        del data['confirmed_email']
        del data['confirmed_code']

    def handle_join_success(self, data):
        email = self.get_confirmed_email()
        storage = RegistrationStorage(self.context)
        storage.remove(email)
        registry = getUtility(IRegistry)
        try:
            review = registry['plone.review_registrations']
        except KeyError:
            review = False
            pass
        if review:
            storage = RegistrationReviewStorage(self.context)
            storage.add(email, data)
            self.request.response.redirect('%s/@@under-review?email=%s' % (
                self.context.absolute_url(), email))
        else:
            return super(RegistrationForm, self).handle_join_success(data)

    def __call__(self):
        if not self.verify():
            return self.request.response.redirect('%s/@@register-confirm-email' % (
                self.context.absolute_url()))

        return super(RegistrationForm, self).__call__()


class IHiddenVerifiedEmail(Interface):

    confirmed_email = schema.TextLine()
    confirmed_code = schema.TextLine()


class EmailConfirmationFormExtender(extensible.FormExtender):
    """Registrationform extender to extend it with the captcha schema.
    """
    adapts(Interface, ILayer, RegistrationForm)
    fields = Fields(IHiddenVerifiedEmail)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        self.captcha = settings.captcha
        portal_membership = getToolByName(self.context, 'portal_membership')
        self.isAnon = portal_membership.isAnonymousUser()

    def update(self):
        self.add(IHiddenVerifiedEmail, prefix="")
        self.form.fields['confirmed_email'].mode = interfaces.HIDDEN_MODE
        self.form.fields['confirmed_code'].mode = interfaces.HIDDEN_MODE


class ReviewRequests(BrowserView):

    def enabled(self):
        registry = getUtility(IRegistry)
        try:
            return registry['plone.review_registrations']
        except KeyError:
            return False

    def send_approve_mail(self, email, data):
        data = data.copy()
        data['url'] = self.context.absolute_url()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "User approved"
        msg['From'] = getUtility(ISiteRoot).email_from_address
        msg['To'] = email
        text = """
Hello %(fullname)s,

The user with username "%(username)s" has been approved.

You can visit the site at: %(url)s
""" % data
        html = """
<p>Hello %(fullname)s,</p>

<p>The user with username "%(username)s" has been approved.</p>

<p>You can visit the site at: <a href="%(url)s">%(url)s</a>
</p>""" % data
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        mailhost = getToolByName(self.context, 'MailHost')
        mailhost.send(msg.as_string())

    def __call__(self):
        storage = RegistrationReviewStorage(self.context)
        if self.request.REQUEST_METHOD == 'POST':
            email = self.request.form.get('email')
            if self.request.form.get('approve'):
                data = storage.get(email).copy()
                data.pop('code')
                data.pop('created')
                reg_form = BaseRegistrationForm(self.context, self.request)
                reg_form.updateFields()
                reg_form.updateWidgets()
                reg_form.handle_join_success(data)
                if data.get('password'):
                    # won't get an email so sent them out something about getting approved
                    self.send_approve_mail(email, data)
                storage.remove(email)
            elif self.request.form.get('deny'):
                storage.remove(email)
            elif self.request.form.get('enable'):
                getUtility(IRegistry)['plone.review_registrations'] = True
            elif self.request.form.get('disable'):
                getUtility(IRegistry)['plone.review_registrations'] = False
        self.storage = storage
        self.data = storage._data
        return self.index()


class UnderReview(BrowserView):

    def __call__(self):
        storage = RegistrationReviewStorage(self.context)
        self.data = storage.get(self.request.form.get('email'))
        return self.index()
