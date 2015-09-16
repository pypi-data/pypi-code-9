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
            for (name, test_name) in self.config.get('db', {}).items():
                for conf in settings.DATABASES.values():
                    if conf["NAME"] == name:
                        conf["NAME"] = test_name
            #self.connection.settings_dict["NAME"] = test_database_name
        else:
            self.set_title('setup', **options)

            # Make a module we can import and use to re-run at will
            if not os.path.isdir(self.am_path):
                os.makedirs(self.am_path)
            with open(self.am_file, 'w') as fhl:
                fhl.write("# Force tests to reload with this file\n")
            print self.am_file

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
        print "Saving config"
        with open(self.config_file, 'w') as fhl:
            fhl.write(json.dumps(self.config))

    def setup_databases(self, **options):
        print "\nPlease wait while your database is created...\n"
        test_runner = self.TestRunner(**options)
        old_config = test_runner.setup_databases()
        atexit.register(self.teardown_autotest, old_config, **options)

        config = {'db': {}}
        from django.conf import settings
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

        setup_test_environment()
        test_runner = self.TestRunner(**options)
        suite = test_runner.build_suite(todo, None)
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

        try:
            tgt = raw_input("\nSelect failures to target (enter to reset): ")
            self.config['todo'] = [failures[int(x)-1] for x in tgt.split(',')]
            self.save_config()
            print "Replaying [%s]" % test
        except:
            # Reset to test_labels by default
            print "Replaying [all]"
            del self.config['todo']
            self.save_config()

        return self.ask_rerun()

    def ask_rerun(self):
        a = raw_input("Run import again [Yn]: ").strip()
        if not a or a.lower()[0] == 'y':
            with open(self.am_file, 'a') as fhl:
                fhl.write('#') 

