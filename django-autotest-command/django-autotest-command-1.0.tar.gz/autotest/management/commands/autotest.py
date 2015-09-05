"""
Replace the test framework with a service that can restart tests as needed
"""

import os
import sys
import atexit

from django.utils import autoreload
from django.core.management.commands.test import Command as BaseCommand


class Command(BaseCommand):
    todo_file = '.failed-tests'
    help = ('Discover and run tests in the specified modules or the current directory and restart when files change to re-run tests.')

    @property
    def TestRunner(self, **options):
        from django.conf import settings
        from django.test.utils import get_runner
        return get_runner(settings, options.get('testrunner'))

    def handle(self, *test_labels, **options):
        from django.conf import settings

        options['verbosity'] = int(options.get('verbosity'))
        if options.get('liveserver') is not None:
            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options['liveserver']
            del options['liveserver']

        if os.path.isfile(self.todo_file):
            print "\n * Running tests!\n"
        else:
            self.set_title('setup', **options)
            print "\nPlease wait while your database is created...\n"
            test_runner = self.TestRunner(**options)
            test_runner.setup_test_environment()
            old_config = test_runner.setup_databases()
            atexit.register(self.at_exit, old_config, **options)
            with open(self.todo_file, 'w') as fhl:
                fhl.write('')
            print "\n -= Testing Service Running; use [CTRL]+[C] to exit =-\n"

        try:
            autoreload.main(self.inner_run, test_labels, options)
        except OSError:
            print "Exiting autorun."

    def set_title(self, text, **options):
        sys.stdout.write("\x1b]2;@test %s\x07" % text)

    def at_exit(self, old_config, **options):
        os.unlink(self.todo_file)
        test_runner = self.TestRunner(**options)
        test_runner.teardown_databases(old_config)
        test_runner.teardown_test_environment()
        print " +++ Test Service Finished"

    def inner_run(self, *test_labels, **options):
        todo = []
        with open(self.todo_file, 'r') as todo_list:
            todo = [ item for item in todo_list.read().split('\n') if item]
        todo = todo or test_labels

        test_runner = self.TestRunner(**options)
        suite = test_runner.build_suite(todo, None)
        result = test_runner.run_suite(suite)

        failures = []
        for test, err in result.errors + result.failures:
            (name, module) = str(test).rsplit(')', 1)[0].split(' (')
            failures.append('%s.%s' % (module, name))

        if not failures:
            if test_labels != todo:
                self.set_title('NOW PASS!')
                print "\nFinally working!\n"
                # Clear error todo (reset to test_labels)
                self.next_todo() 
            else:
                self.set_title('PASS')
                print "\nStill working!\n"
            return
        
        # Add all failues to next todo list (for re-run)
        self.next_todo(*failures)
        self.set_title('FAIL [%d]' % len(failures))
        # Print options for user to select test target but
        # also set all failed tests as targets
        with open(self.todo_file, 'w') as todo_list:
            for x, test in enumerate(failures):
                todo_list.write(test + '\n')
                print "  %d. %s " % (x+1, test)

        try:
            tgt = raw_input("\nSelect failures to target (enter to reset): ")
            new_todos = [failures[int(x)-1] for x in tgt.split(',')]
        except:
            # Reset to test_labels by default
            print "Replaying [all]"
            self.next_todo()
        else:
            print "Replaying [%s]" % test
            self.next_todo(*new_todos)

    def next_todo(self, *new_todos):
        with open(self.todo_file, 'w') as todo_list:
            for todo in new_todos:
                todo_list.write(todo+'\n')

