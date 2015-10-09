# standard library imports
import datetime
import logging
import uuid

from urllib import quote

# third-party imports
from cherrypy import request, NotFound
from turbogears import (config, controllers, expose, error_handler, flash,
    identity, redirect, url, validate, validators, visit)
from turbogears.view import variable_providers

# project specific imports
from spammcan.model import Format, Paste, Style, session
# from spammcan import json
from spammcan.forms import (paste_form, Range, style_select, ValidPasteGuid,
    ValidStyle)
from spammcan.release import version as sc_version
from spammcan.util import (absolute_url, add_global_tmpl_vars, code2html,
    get_user_id, get_server_name, get_static_content, txt2html, wrap_text)


log = logging.getLogger("spammcan.controllers")
variable_providers.append(add_global_tmpl_vars)


class Root(controllers.RootController):
    """The root controller of the application."""

    @expose(template="spammcan.templates.paste")
    @validate(validators=dict(
        paste=ValidPasteGuid(),
        hl=Range(if_invalid=None),
        ln=validators.StringBoolean(if_invalid=True),
        st=ValidStyle(if_invalid=None, convert_value=False),
        wrap=validators.Int(if_invalid=None)))
    def index(self, paste=None, hl=None, ln=True, st=None, wrap=80,
            tg_errors=None):
        """"Show the paste given by GUID."""
        if tg_errors:
            flash(_(u'Paste not found.'))
            paste = None
        #log.debug("Paste: %s", paste)
        if paste is None:
            redirect('/new')

        try:
            if wrap:
                wrapped_lines, code = wrap_text(paste.code, wrap)
                if wrapped_lines:
                    hl = set(hl or [])
                    hl.update(wrapped_lines)
                    hl = list(hl)
                    flash(_(u"Some long lines have been wrapped at %i chars "
                        "and highlighted. Add '?wrap=no' to the paste URL to "
                        "disable line wrapping.") % wrap)
            else:
                code = paste.code
            html, css = code2html(code, paste.format.name, style=st,
                hl_lines=hl, linenos=ln)
        except:
            log.exception('Syntax highlighting error.')
            flash(_(u'Internal error. Syntax highlighting disabled.'))
            html = '<pre class="source">%s</pre>' % paste.code
            css = None
        #log.debug("Pygments output: %s", html)

        # make URL for "Send link" link
        subject = _(u"Link for paste '%s' on %s") % (paste.title or
            _(u"untitled"), get_server_name())
        paste_url = absolute_url(['/paste', paste.guid], st=st)
        mailto_url = 'mailto:?subject=%s&body=%s' % (quote(subject, ''),
            quote(paste_url, ''))

        styles = list(Style.options())
        pagetitle = _(u"Serving paste '%s' fresh from the SpammCan") % (
            paste.title or 'untitled',)
        paste.last_access = datetime.datetime.now()
        session.flush()
        return dict(
            paste = paste,
            pretty_code = html,
            css = css,
            pagetitle = pagetitle,
            mailto_url = mailto_url,
            lineno = not ln,
            style_select = style_select,
            form_values = dict(st=st or 'default'),
            form_params = dict(
                action=url(['/paste', paste.guid]),
                child_args=dict(st={'options': styles})))
    paste = index

    @expose(content_type="text/plain")
    @validate(validators=dict(paste=ValidPasteGuid()))
    def download(self, paste, tg_errors=None, *args, **kw):
        """Serve the paste given by GUID as plain text."""
        if tg_errors:
            raise NotFound
        paste.last_access = datetime.datetime.now()
        session.flush()
        return paste.code

    @expose(template="spammcan.templates.new")
    @validate(validators=dict(paste=ValidPasteGuid(if_invalid=None)))
    def new(self, paste=None, tg_errors=None):
        """Show the form for a new paste."""
        formats = list(Format.options())
        if paste:
            code = paste.code
            format = paste.format.name
            title = paste.title
            if title and not title.startswith('Re: '):
                title = _(u'Re: ') + title
        else:
            code = None
            format = 'text'
            title = None
        return dict(
            form = paste_form,
            values = {
                'format': format,
                'submit': _(u'Spamm me!'),
                'code': code,
                'title': title},
            params = dict(
                action = url('/create'),
                child_args = dict(format={'options': formats})
            ))

    @expose(template="spammcan.templates.paste")
    @validate(form=paste_form)
    @error_handler(new)
    def create(self, code, format=None, title=None):
        """Save submitted paste and redirect to '/paste' to show it."""
        guid = uuid.uuid4().hex
        #log.debug("GUID: %(guid)r, format: %(format)r, title: %(title)r, "
        #    "Code: %(code)r", locals())
        uid = get_user_id()
        paste = Paste(guid=guid, format=format, code=code, title=title,
            creator=uid)
        session.save(paste)
        session.flush()
        redirect(['/paste', guid])

    @expose(template='spammcan.templates.list')
    def mypastes(self, uid=None):
        uid = uid or get_user_id()
        pastes = Paste.query().filter_by(creator=uid).order_by(
            Paste.last_access.desc())
        pagetitle = _(u'Your pastes')
        return dict(pastes=pastes, pagetitle=pagetitle, uid=uid)

    @expose(template="spammcan.templates.static")
    def about(self, package=None):
        """Display information page about the software."""
        content = get_static_content('about.rst')
        return dict(
            pagetitle = _(u'About'),
            heading = _(u'About this site'),
            content = content,
            message = _(u'This site is powered by SpammCan version %s.'
                ) % sc_version
        )

    @expose(template="spammcan.templates.static")
    def help(self, package=None):
        """Display usage information for the software."""
        content = get_static_content('help.rst')
        return dict(
            pagetitle = _(u'Help'),
            heading = _(u'How to use the SpammCan'),
            content = content
        )

    @expose(template="spammcan.templates.login")
    def login(self, forward_url=None, *args, **kw):
        """Show the login form or forward user to previously requested page."""

        if forward_url:
            if isinstance(forward_url, list):
                forward_url = forward_url.pop(0)
            else:
                del request.params['forward_url']

        new_visit = visit.current()
        if new_visit:
            new_visit = new_visit.is_new

        if (not new_visit and not identity.current.anonymous
                and identity.was_login_attempted()
                and not identity.get_identity_errors()):
            redirect(forward_url or '/', kw)

        if identity.was_login_attempted():
            if new_visit:
                msg = _(u"Cannot log in because your browser "
                         "does not support session cookies.")
            else:
                msg = _(u"The credentials you supplied were not correct or "
                         "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg = _(u"You must provide your credentials before accessing "
                     "this resource.")
        else:
            msg = _(u"Please log in.")
            if not forward_url:
                forward_url = request.headers.get("Referer", "/")

        # we do not set the response status here anymore since it
        # is now handled in the identity exception.
        return dict(logging_in=True, message=msg,
            forward_url=forward_url, previous_url=request.path_info,
            original_parameters=request.params)

    @expose()
    def logout(self):
        """Log out the current identity and redirect to start page."""
        identity.current.logout()
        redirect("/")
