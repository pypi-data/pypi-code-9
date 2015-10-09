from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from optparse import make_option

User = get_user_model()


class Command(BaseCommand):
    __OPTION_NAME_IS_SUPERUSER = "superuser"
    __OPTION_NAME_IS_STAFF = "staff"
    __OPTION_NAME_EMAIL = "email"
    __OPTION_NAME_FIRST_NAME = "firstName"
    __OPTION_NAME_LAST_NAME = "lastName"

    args = '<USERNAME> <PASSWORD>'
    help = 'Create a test user with the given name and password if the username does not exist.'
    option_list = BaseCommand.option_list + (
        make_option('--' + __OPTION_NAME_IS_SUPERUSER, action='store_true',
                    help='Should the new user be superuser', default=False),
        make_option('--' + __OPTION_NAME_IS_STAFF, action='store_true',
                    help='Should the new user be staff', default=False),
        make_option('--' + __OPTION_NAME_EMAIL, action='store',
                    help='Email of the new user', default=None),
        make_option('--' + __OPTION_NAME_FIRST_NAME, action='store',
                    help='First name of the new user', default=None),
        make_option('--' + __OPTION_NAME_LAST_NAME, action='store',
                    help='Last name of the new user', default=None))

    def handle(self, *args, **options):

        if len(args) != 2:
            raise CommandError("Expected <USERNAME> <PASSWORD> arguments")

        username = args[0]
        password = args[1]

        if User.objects.filter(username=username):
            print("User with name '{}' already exists.".format(username))
            return

        u = User(username=username, email=options[Command.__OPTION_NAME_EMAIL])
        if options[Command.__OPTION_NAME_EMAIL]:
            u.email = options[Command.__OPTION_NAME_EMAIL]
        if options[Command.__OPTION_NAME_FIRST_NAME]:
            u.first_name = options[Command.__OPTION_NAME_FIRST_NAME]
        if options[Command.__OPTION_NAME_LAST_NAME]:
            u.last_name = options[Command.__OPTION_NAME_LAST_NAME]
        u.set_password(password)
        u.is_superuser = options[Command.__OPTION_NAME_IS_SUPERUSER]
        u.is_staff = options[Command.__OPTION_NAME_IS_STAFF]
        u.save()

        print("Created user with name '{}'".format(username))
