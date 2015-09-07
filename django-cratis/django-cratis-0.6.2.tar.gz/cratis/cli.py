import os
import sys

class NotProperlyConfigured(Exception):
    pass


class NoVariableDefined(NotProperlyConfigured):
    def __init__(self, var_name, *args, **kwargs):
        super(NoVariableDefined, self).__init__(*args, **kwargs)
        self.var_name = var_name


class NoConfigFile(NotProperlyConfigured):
    pass


class NoCratisApp(NotProperlyConfigured):
    pass


def load_env():
    os.environ['DJANGO_CONFIGURATION'] = os.environ.get('DJANGO_CONFIGURATION', 'Dev')
    os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get('DJANGO_SETTINGS_MODULE', 'settings')

    app_path = os.environ.get('CRATIS_APP_PATH', os.getcwd())
    sys.path += (app_path, )


def cratis_cmd():
    """
    Command that executes django ./manage.py task + loads environment variables from cratis.yml

    Command also can be executed from sub-folders of project.
    """

    try:
        load_env()

        from configurations.management import execute_from_command_line

        execute_from_command_line(sys.argv)

    except NotProperlyConfigured as e:
        print('\n\tError: %s\n' % e.message)


class AlreadyExistsException(Exception):
    pass

