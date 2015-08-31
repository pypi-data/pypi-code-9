from django.conf.urls import patterns, url
from django.contrib import admin

from admin_sso import settings
from admin_sso.models import Assignment


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'username', 'username_mode', 'domain',
                    'user', 'weight')
    list_editable = ('username', 'username_mode', 'domain', 'user', 'weight')

    def get_urls(self):
        urls = super(AssignmentAdmin, self).get_urls()
        opts = self.model._meta
        try:
            #  Django 1.8 only provides model_name
            info = (opts.app_label, opts.model_name)
        except AttributeError:
            info = (opts.app_label, opts.module_name)

        return patterns('admin_sso.views',
            url(r'^start/$', 'start',
                name='%s_%s_start' % info),
            url(r'^end/$', 'end',
                name='%s_%s_end' % info),
        ) + urls

admin.site.register(Assignment, AssignmentAdmin)


if settings.DJANGO_ADMIN_SSO_ADD_LOGIN_BUTTON:
    admin.site.login_template = 'admin_sso/login.html'
