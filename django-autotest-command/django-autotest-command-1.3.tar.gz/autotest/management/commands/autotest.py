"""
Replace the test framework with a service that can restart tests as needed
"""

import os
import sys
import json
import atexit

from django.utils import autoreload
from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management.commands.test import Command as BaseCommand


class Command(BaseCommand):
    config_file = '.autotest.conf'
    auto_module = ('/', 'tmp', 'autotest', 'at_lib')
    am_path = property(lambda self: os.path.join(*self.auto_module[:-1]))
    am_file = property(lambda self: os.path.join(*self.auto_module)+'.py')
    help = ('Discover and run tests in the specified modules or the current directory and restart when files change to re-run tests.')

    @property
    def TestRunner(self, **options):
        from django.conf import settings
        from django.test.utils import get_runner
        return get_runner(settings, options.get('testrunner'))

    def handle(self, *test_labels, **options):
        self.config = {}

        options['verbosity'] = int(options.get('verbosity'))
        if options.get('liveserver') is not None:
            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options['liveserver']
            del options['liveserver']

        if os.path.isfile(self.config_file):
            print "\n * Running tests!\n"
            from django.conf import settings
            with open(self.config_file, 'r') as fhl:
                self.config = json.loads(fhl.read())
            for (orig_name, test_name) in self.config.get('db', {}).items():
                for (db_name, conf) in settings.DATABASES.items():
                    #self.flush_database(name)
                    if conf["NAME"] == orig_name:
                        conf["NAME"] = test_name
                        #print "DB SET: %s -> %s" % (orig_name, test_name)

            settings.DEBUG = False
        else:
            self.set_title('setup', **options)

            # Make a module we can import and use to re-run at will
            if not os.path.isdir(self.am_path):
                os.makedirs(self.am_path)
            with open(self.am_file, 'w') as fhl:
                fhl.write("# Force tests to reload with this file\n")

            self.config = self.setup_databases(**options)
            self.save_config()

            print "\n -= Testing Service Running; use [CTRL]+[C] to exit =-\n"

        sys.path.append(self.am_path)
        try:
            __import__(self.auto_module[-1])
        except ImportError:
            self.teardown_autotest((([]),[]))
            print("Config error, I've cleaned up, please try again.")
            sys.exit(2)

        try:
            autoreload.main(self.inner_run, test_labels, options)
        except OSError:
            print "Exiting autorun."

    def save_config(self):
        with open(self.config_file, 'w') as fhl:
            fhl.write(json.dumps(self.config))

    def setup_databases(self, **options):
        test_runner = self.TestRunner(**options)
        old_config = test_runner.setup_databases()
        atexit.register(self.teardown_autotest, old_config, **options)

        config = {'db': {}}
        for conf in old_config[0]:
            config['db'][conf[1]] = conf[0].settings_dict['NAME']
        return config

    def set_title(self, text, **options):
        sys.stdout.write("\x1b]2;@test %s\x07" % text)

    def teardown_autotest(self, old_config, **options):
        for f in (self.config_file, self.am_file, self.am_file+'c', self.am_path):
            if os.path.isfile(f):
                os.unlink(f)
            elif os.path.isdir(f):
                os.rmdir(f)
        test_runner = self.TestRunner(**options)
        test_runner.teardown_databases(old_config)
        print " +++ Test Service Finished"

    def inner_run(self, *test_labels, **options):
        todo = self.config.get('todo', test_labels)
        if '*' in todo:
            todo = []

        setup_test_environment()
        test_runner = self.TestRunner(**options)
        try:
            suite = test_runner.build_suite(todo, None)
        except ImportError:
            print "Error, selected test module can't be found: %s" % str(todo)
            return self.ask_rerun()
        except AttributeError:
            print "Error, selected test function can't be found: %s" % str(todo)
            return self.ask_rerun()

        result = test_runner.run_suite(suite)
        teardown_test_environment()

        failures = []
        for test, err in result.errors + result.failures:
            (name, module) = str(test).rsplit(')', 1)[0].split(' (')
            failures.append('%s.%s' % (module, name))

        if not failures:
            if test_labels != todo:
                self.set_title('NOW PASS!')
                print "\nFinally working!\n"
                # Clear error todo (reset to test_labels)
                del self.config['todo']
                self.save_config()
            else:
                self.set_title('PASS')
                print "\nStill working!\n"
            return self.ask_rerun()
        
        # Add all failues to next todo list (for re-run)
        self.config['todo'] = failures
        self.save_config()

        self.set_title('FAIL [%d]' % len(failures))
        # Print options for user to select test target but
        # also set all failed tests as targets
        for x, test in enumerate(failures):
            print "  %d. %s " % (x+1, test)

        return self.ask_rerun(failures)

    def flush_database(self, db_name):
        """Remove all data that might be in a database left over"""
        from django.core.management import call_command
        call_command('flush', verbosity=0, interactive=False, database=db_name,
                     skip_checks=True, reset_sequences=False, allow_cascade=True,
                     inhibit_post_migrate=False)


    def ask_rerun(self, failures=None):
        rerun = raw_input("Select failures to target or press enter to re-run all: ").strip()
        self.config['todo'] = list(self.get_selection(rerun, failures))
        self.save_config()
        if rerun != '-':
            with open(self.am_file, 'a') as fhl:
                fhl.write('#') 

    def get_selection(self, rerun, failures):
        for failure in rerun.split(','):
            failure = failure.strip()
            if failure.isdigit() and failures:
                yield failures[int(failure)-1]
            elif failure:
                yield failure
    
