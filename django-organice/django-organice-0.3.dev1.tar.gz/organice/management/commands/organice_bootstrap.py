"""
Management commands for django Organice.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from cms.api import create_page
from cms.models import Title


def create_user(username):
    print(u"Creating user {} with password {} ...".format(username, username))
    try:
        User.objects.get(username=username).delete()
        print(u"Warning: deleted existing user {} first.".format(username))
    except User.DoesNotExist:
        pass
    User.objects.create_user(username, 'testuser@notch-interactive.com', username).save()


def delete_page(title):
    """Delete all pages with the given title."""
    while len(Title.objects.filter(title=title)):
        # Pain! filter, because django CMS creates 2 titles for each page
        page = Title.objects.filter(title=title).first().page
        print(u"Warning: deleting existing page {} first ...".format(title))
        page.delete()


def add_cms_page(title, template='cms_base.html'):
    print(u"Creating page {} ...".format(title))
    delete_page(title)
    create_page(title, template, language='en', in_navigation=True, published=True)


class Command(BaseCommand):
    help = 'Organice management commands.'

    def handle(self, *args, **options):
        self.stdout.write('Initialize database ...')
        call_command('migrate')

        self.stdout.write('Create admin user ...')
        # call_command('createsuperuser', '--username', 'admin', '--email', 'you@example.com', '--noinput')
        u = User.objects.get(username='admin')
        u.set_password('admin')
        u.save()

        self.stdout.write('Generate menu structure ...')
        add_cms_page(_('Home'))

        self.stdout.write('Have an organiced day!')
