import json
import re
import copy
import datetime
import logging
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.core.urlresolvers import resolve
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from blacklist import utils
from django.contrib.gis.geoip import GeoIP, GeoIPException
try:
    g = GeoIP()
except GeoIPException:
    g = None

logger = logging.getLogger(__name__)

blacklisting = getattr(settings, 'BLACKLISTING', {})
_ip_header = blacklisting.get('REMOTE_IP_HEADER', 'REMOTE_ADDR')
_auto_blocking_rules = blacklisting.get('AUTO_BLOCKING_RULES', ())
permission_denied_callback = blacklisting.get('PERMISSION_DENIED_CALLBACK', 'blacklist.utils.permission_denied_default')

AUTO_BLOCKING_RULES_DEFAULTS = {
    'RULE': {
        'ip': '-',
        'user_agent': '-',
        'user_agent_re': False,
        'method': '-',
        'view': '-',
        'path': '-',
        'path_re': False
    },
    'PERIOD': datetime.timedelta(days=30),
    'BLOCK_AFTER': 1000,
    'ENABLED': True,
    'PROPOSAL': True,
    'NOTIFY': settings.MANAGERS
}


def _get_ip(meta):
    ip = None
    if isinstance(_ip_header, str):
        ip = meta.get(_ip_header)
    elif isinstance(_ip_header, (tuple, list)):
        for header_name in _ip_header:
            ip = meta.get(header_name)
            if ip:
                break
    elif callable(_ip_header):
        ip = _ip_header(meta)
    return ip


class RequestLogManager(models.Manager):
    def log_request(self, request):
        """
        Create RequestLog object from request
        :return: RequestLog object
        """
        resolver_match = resolve(request.path)
        view = resolver_match.url_name if resolver_match.url_name != 'blacklist.utils.Decorator' else None
        if view and resolver_match.namespace:
            view = '{ns}:{name}'.format(ns=resolver_match.namespace, name=resolver_match.url_name,)
        return self.create(ip=_get_ip(request.META),
                           user_agent=request.META.get('HTTP_USER_AGENT', 'unknown'),
                           method=request.method,
                           path=request.path,
                           view=view)

    def create_blocking_rules(self):
        """Create blocking rules based on settings.AUTO_BLOCKING_RULES and RequestLog model data"""
        result = list()
        for setting_no, short_blocking_setting in enumerate(_auto_blocking_rules):
            if not short_blocking_setting.get('ENABLED', True):
                continue
            # build full setting
            blocking_setting = copy.deepcopy(AUTO_BLOCKING_RULES_DEFAULTS)
            short_blocking_setting = dict(short_blocking_setting)
            short_blocking_rule = short_blocking_setting.pop('RULE', {})
            blocking_setting.update(short_blocking_setting)
            short_blocking_setting['RULE'] = short_blocking_rule
            blocking_setting['RULE'].update(short_blocking_rule)
            blocking_rule = blocking_setting['RULE']
            # Counting amount of RequestLog that applies setting rule
            rule = models.Q()
            group_by = []
            for key in ('ip', 'user_agent', 'method', 'path', 'view'):
                if blocking_rule[key] != '-':
                    rule &= models.Q(**{key+'__regex': blocking_rule[key]})
                    if key in ('user_agent', 'path'):
                        if not blocking_rule[key+'_re']:
                            group_by.append(key)
                    else:
                        group_by.append(key)
            if not rule:
                logger.error('Not found any blocking rule in setting %d. Setting missed' % setting_no)
                continue
            query_set = self.filter(rule).filter(created__gte=datetime.datetime.now() - blocking_setting['PERIOD'])
            query_set = query_set.values(*group_by).annotate(models.Count('pk')).filter(pk__count__gte=blocking_setting['BLOCK_AFTER'])
            created_rules = list()
            for matched in query_set.all():
                params = dict((key, matched[key]) for key in group_by)
                for key in ('user_agent', 'path'):
                    if blocking_rule[key] != '-' and key not in params:
                        params[key] = blocking_rule[key]
                # params['enabled'] = not blocking_setting['PROPOSAL']
                rule, created = BlockRules.objects.get_or_create(**params)
                if created:
                    rule.enabled = not blocking_setting['PROPOSAL']
                    rule.save()
                    created_rules.append(rule)
            if created_rules:
                result.extend(created_rules)
                if blocking_setting['NOTIFY']:
                    self._notify_users(
                        created_rules, short_blocking_setting,
                        not blocking_setting['PROPOSAL'], [n[1] for n in blocking_setting['NOTIFY']])
        return result

    def _notify_users(self, rules, setting, enabled, emails):
        title = __('New Block Rules have been created')
        message = get_template('blacklist/email_notification.tmpl.html')
        site = None
        try:
            from django.contrib.sites.models import Site
            site = Site.objects.get_current()
        except ImproperlyConfigured as e:
            logger.warning("In order to send users site url in e-mail please enable and configure site framework")
        message = message.render(Context(dict(title=title, enable=enabled, rules=rules, site=site,
                                              setting=json.dumps(setting, indent=2, sort_keys=True,
                                                                 default=utils.dt_json_serializer))))
        send_mail(title, '', settings.DEFAULT_FROM_EMAIL, emails, html_message=message)


class RequestLog(models.Model):
    ip = models.GenericIPAddressField(_('Client IP'), protocol='IPv4', null=True)
    user_agent = models.CharField(_('User Agent'), max_length=256, null=True)
    method = models.CharField(_('HTTP method'), max_length=7, null=False)
    path = models.SlugField(_('Request Path'), db_index=False, null=False)
    view = models.CharField(_('Request View'), max_length=100, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    objects = RequestLogManager()

    @property
    def country(self):
        if g:
            return '{country_name} ({country_code})'.format(**g.country(self.ip))
        return 'Unknown'

    class Meta:
        verbose_name = _('Request Log')
        verbose_name_plural = _('Request Logs')


class BlockRulesManager(models.Manager):
    def match(self, request):
        """
        Checks request object for matching blocking rules
        :param request: Django request object
        :return: rule if blacklisted, False if white-listed, None if not found
        """
        for rule in self.filter(enabled=False).defer('enabled', 'created', 'updated'):
            if rule.match(request):
                return False   # white-listed
        for rule in self.filter(enabled=True).defer('enabled', 'created', 'updated'):
            if rule.match(request):
                return rule    # black-listed
        return None  # not found


class BlockRules(models.Model):
    ip = models.GenericIPAddressField(_('Client IP'), protocol='IPv4', null=True, blank=True)
    user_agent = models.CharField(_('User Agent'), max_length=256, null=True, blank=True,
                                  help_text=_('You can specify regexp here'))
    method = models.CharField(_('HTTP method'), max_length=7, null=True, blank=True,
                              help_text=_('Empty value means any type of request'))
    country = models.ForeignKey('Country', null=True, blank=True, verbose_name=_('Country'))
    path = models.CharField(_('Request Path'), max_length=200, db_index=False, null=True, blank=True,
                            help_text=_('You can specify regexp here'))
    view = models.CharField(_('Request View'), max_length=100, null=True, blank=True)
    enabled = models.BooleanField(_('Enabled'), default=False, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlockRulesManager()

    class Meta:
        verbose_name = _('Block Rule')
        verbose_name_plural = _('Block Rules')

    def match(self, request):
        """
        Check request for matching blocking rule
        :return: True if matches else False
        """
        current_ip = _get_ip(request.META)
        if not self.ip or current_ip == self.ip:
            if not self.country_id or not g or g.country(current_ip)['country_code'] == self.country_id:
                if (not self.user_agent or request.META.get('HTTP_USER_AGENT', 'unknown') == self.user_agent or
                        re.match(self.user_agent, request.META.get('HTTP_USER_AGENT', 'unknown'))):
                    if not self.method or self.method.lower() == request.method.lower():
                        if (not self.path or self.path == request.path or
                                re.match(self.path, request.path)):
                            if not self.view or resolve(request.path).url_name == self.view:
                                return True
        return False


class Country(models.Model):
    code = models.CharField(_('Country code'), primary_key=True, max_length=2)
    title = models.CharField(_('Country name'), max_length=255)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('code',)

    def __str__(self):
        return '{0.code}({0.title})'.format(self)
