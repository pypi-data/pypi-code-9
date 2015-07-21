
#          Copyright Jamie Allsop 2013-2015
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

#-------------------------------------------------------------------------------
#   RunProcessTest
#-------------------------------------------------------------------------------

import os
import sys
import shlex

import cuppa.timer
import cuppa.progress
from cuppa.output_processor import IncrementalSubProcess


class TestSuite(object):

    suites = {}

    @classmethod
    def create( cls, name, scons_env ):
        if not name in cls.suites:
            cls.suites[name] = TestSuite( name, scons_env )
        return cls.suites[name]

    def __init__( self, name, scons_env ):
        self._name = name
        self._scons_env = scons_env
        self._colouriser = scons_env['colouriser']

        sys.stdout.write('\n')
        sys.stdout.write(
            self._colouriser.emphasise( "Starting Test Suite [{}]".format( name ) )
        )
        sys.stdout.write('\n')

        cuppa.progress.NotifyProgress.register_callback( scons_env, self.on_progress )

        self._suite = {}
        self._suite['total_tests']       = 0
        self._suite['passed_tests']      = 0
        self._suite['failed_tests']      = 0
        self._suite['expected_failures'] = 0
        self._suite['skipped_tests']     = 0
        self._suite['aborted_tests']     = 0
        self._suite['total_cpu_times']   = cuppa.timer.CpuTimes( 0, 0, 0, 0 )

        self._tests = []


    def on_progress( self, progress, sconscript, variant, env, target, source ):
        if progress == 'finished':
            self.exit_suite()
            suite = env['build_dir']
            del self.suites[suite]


    def enter_test( self, test, expected='success' ) :
        sys.stdout.write(
            self._colouriser.emphasise( "\nTest [%s]..." % test ) + '\n'
        )
        self._tests.append( {} )
        test_case = self._tests[-1]
        test_case['name']     = test
        test_case['expected'] = expected
        test_case['timer']    = cuppa.timer.Timer()


    def exit_test( self, test, status='success' ):
        test_case = self._tests[-1]
        test_case['timer'].stop()
        test_case['status'] = status

        self._write_test_case( test_case )

        self._suite['total_tests'] += 1
        if status == 'success':
            self._suite['passed_tests'] += 1
        elif status == 'failed':
            self._suite['failed_tests'] += 1
        elif status == 'expected_failure':
            self._suite['expected_failures'] += 1
        elif status == 'aborted':
            self._suite['aborted_tests'] += 1
        elif status == 'skipped':
            self._suite['skipped_tests'] += 1

        self._suite['total_cpu_times'] += test_case['timer'].elapsed()

        sys.stdout.write('\n\n')


    def _write_test_case( self, test_case ):
        expected = test_case['expected'] == test_case['status']
        passed   = test_case['status'] == "success"
        meaning  = test_case['status']

        if not expected and passed:
            meaning = 'unexpected_success'

        label = " ".join( meaning.upper().split('_') )

        cpu_times = test_case['timer'].elapsed()
        sys.stdout.write( self._colouriser.highlight( meaning, " = %s = " % label ) )
        cuppa.timer.write_time( cpu_times, self._colouriser )


    def exit_suite( self ):

        suite = self._suite

        total_tests  = suite['total_tests']
        passed_tests = suite['passed_tests'] + suite['expected_failures'] + suite['skipped_tests']
        failed_tests = suite['failed_tests'] + suite['aborted_tests']

        expected_failures = suite['expected_failures']
        skipped_tests     = suite['skipped_tests']
        aborted_tests     = suite['aborted_tests']

        suite['status'] = 'passed'
        meaning = 'success'

        if total_tests != passed_tests:
            suite['status'] = 'failed'
            meaning = 'failed'

        sys.stdout.write(
            self._colouriser.emphasise( "\nTest Suite [{}] ".format( self._name ) )
        )

        sys.stdout.write(
            self._colouriser.highlight( meaning, " = {} = ".format( suite['status'].upper() ) )
        )

        sys.stdout.write('\n')

        sys.stdout.write(
            self._colouriser.emphasise( "\nSummary\n" )
        )

        for test in self._tests:
            sys.stdout.write(
                self._colouriser.emphasise( "\nTest case [{}]".format( test['name'] ) ) + '\n'
            )
            self._write_test_case( test )

        sys.stdout.write('\n\n')

        if total_tests > 0:
            if suite['status'] == 'passed':
                sys.stdout.write(
                    self._colouriser.highlight(
                        meaning,
                        " ( %s of %s Test Cases Passed )" % ( passed_tests, total_tests )
                    )
                )
            else:
                sys.stdout.write(
                    self._colouriser.highlight(
                        meaning,
                        " ( %s of %s Test Cases Failed )" % (failed_tests, total_tests)
                    )
                )
        else:
            sys.stdout.write(
                self._colouriser.colour(
                    'notice',
                    " ( No Test Cases Checked )"
                )
            )

        if passed_tests > 0:
            sys.stdout.write(
                self._colouriser.highlight(
                    meaning,
                    " ( %s %s Passed ) "
                    % (passed_tests, passed_tests > 1 and 'Test Cases' or 'Test Case')
                )
            )

        if failed_tests > 0:
            sys.stdout.write(
                self._colouriser.highlight(
                    meaning,
                    " ( %s %s Failed ) "
                    % (failed_tests, failed_tests > 1 and 'Test Cases' or 'Test Case')
                )
            )

        if expected_failures > 0:
            meaning = 'expected_failure'
            sys.stdout.write(
                self._colouriser.highlight(
                    meaning,
                    " ( %s %s Expected ) "
                    % (expected_failures, expected_failures > 1 and 'Failures' or 'Failure')
                )
            )

        if skipped_tests > 0:
            meaning = 'skipped'
            sys.stdout.write(
                self._colouriser.highlight(
                    meaning,
                    " ( %s %s Skipped ) "
                    % (skipped_tests, skipped_tests > 1 and 'Test Cases' or 'Test Case')
                )
            )

        if aborted_tests > 0:
            meaning = 'aborted'
            sys.stdout.write(
                self._colouriser.highlight(
                    meaning,
                    " ( %s %s Aborted ) "
                    % (aborted_tests, aborted_tests > 1 and 'Test Cases Were' or 'Test Case Was')
                )
            )


        sys.stdout.write('\n')
        cuppa.timer.write_time( self._suite['total_cpu_times'], self._colouriser, True )

        self._tests = []
        self._suite = {}

        sys.stdout.write('\n\n')


    def message(self, line):
        sys.stdout.write(
            line + "\n"
        )


def stdout_file_name_from( program_file ):
    return program_file + '.stdout.log'


def stderr_file_name_from( program_file ):
    return program_file + '.stderr.log'


def success_file_name_from( program_file ):
    return program_file + '.success'


class RunProcessTestEmitter(object):

    def __init__( self, final_dir ):
        self._final_dir = final_dir


    def __call__( self, target, source, env ):
        program_file = os.path.join( self._final_dir, os.path.split( source[0].path )[1] )
        target = []
        target.append( stdout_file_name_from( program_file ) )
        target.append( stderr_file_name_from( program_file ) )
        target.append( success_file_name_from( program_file ) )
        return target, source


class ProcessStdout(object):

    def __init__( self, show_test_output, log ):
        self._show_test_output = show_test_output
        self.log = open( log, "w" )


    def __call__( self, line ):
        self.log.write( line + '\n' )
        if self._show_test_output:
            sys.stdout.write( line + '\n' )


    def __exit__( self, type, value, traceback ):
        if self.log:
            self.log.close()


class ProcessStderr(object):

    def __init__( self, show_test_output, log ):
        self._show_test_output = show_test_output
        self.log = open( log, "w" )


    def __call__( self, line ):
        self.log.write( line + '\n' )
        if self._show_test_output:
            sys.stderr.write( line + '\n' )


    def __exit__( self, type, value, traceback ):
        if self.log:
            self.log.close()


class RunProcessTest(object):

    def __init__( self, expected ):
        self._expected = expected


    def __call__( self, target, source, env ):

        executable = str( source[0].abspath )
        working_dir, test = os.path.split( executable )
        program_path = source[0].path
        suite = env['build_dir']

        if cuppa.build_platform.name() == "Windows":
            executable = '"' + executable + '"'

        test_command = executable

        test_suite = TestSuite.create( suite, env )

        test_suite.enter_test( test, expected=self._expected )

        show_test_output = env['show_test_output']

        try:
            return_code = self.__run_test( show_test_output,
                                           program_path,
                                           test_command,
                                           working_dir )

            if return_code < 0:
                self.__write_file_to_stderr( stderr_file_name_from( program_path ) )
                print >> sys.stderr, "cuppa: ProcessTest: Test was terminated by signal: ", -return_code
                test_suite.exit_test( test, 'aborted' )
            elif return_code > 0:
                self.__write_file_to_stderr( stderr_file_name_from( program_path ) )
                print >> sys.stderr, "cuppa: ProcessTest: Test returned with error code: ", return_code
                test_suite.exit_test( test, 'failed' )
            else:
                test_suite.exit_test( test, 'success' )

            if return_code:
                self._remove_success_file( success_file_name_from( program_path ) )
            else:
                self._write_success_file( success_file_name_from( program_path ) )

            return None

        except OSError, e:
            print >> sys.stderr, "Execution of [", test_command, "] failed with error: ", e
            return 1


    def _write_success_file( self, file_name ):
        with open( file_name, "w" ) as success_file:
            success_file.write( "success" )


    def _remove_success_file( self, file_name ):
        try:
            os.remove( file_name )
        except:
            pass


    def __run_test( self, show_test_output, program_path, test_command, working_dir ):
        process_stdout = ProcessStdout( show_test_output, stdout_file_name_from( program_path ) )
        process_stderr = ProcessStderr( show_test_output, stderr_file_name_from( program_path ) )

        return_code = IncrementalSubProcess.Popen2( process_stdout,
                                                    process_stderr,
                                                    shlex.split( test_command ),
                                                    cwd=working_dir )
        return return_code


    def __write_file_to_stderr( self, file_name ):
        error_file = open( file_name, "r" )
        for line in error_file:
            print >> sys.stderr, line
        error_file.close()

