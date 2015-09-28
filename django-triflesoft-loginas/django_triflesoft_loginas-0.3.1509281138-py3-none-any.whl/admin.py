from django.contrib.admin.sites import site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def login_as(self):
    return "<a href='{0}?id={1}' target='_blank'>Login as {2}</a>".format(reverse('login_as'), self.id, self.get_full_name())


UserAdmin.list_display += ('login_as', )

User.login_as = login_as
User.login_as.allow_tags = True

site.unregister(User)
site.register(User, UserAdmin)
