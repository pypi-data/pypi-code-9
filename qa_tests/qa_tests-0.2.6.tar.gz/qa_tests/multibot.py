#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module is a parallel executor for Robot Framework test suites.
# This launcher supports all Robot Framework command line options and adds the following option:
# '--processes N' where N is the number parallel executors to use (default is cpu count)
#
# Ex. : multibot --processes 4 --robotoption1 --robotoption2 testsuite1 testsuite2


import os
import sys
import shutil
from multiprocessing import Process, Pool, Queue
from robot.running.builder import TestSuiteBuilder
from robot.conf import RobotSettings
from robot import run as run_robot_framework
from robot.run import RobotFramework
from robot.errors import DataError, Information


# Get testsuites list in a sub process
# On huge testsuites, the executable TestSuite object consumes a large amount of memory
# Use it in a sub process ensures a full memory liberation after the job
def sub_get_testsuites(queue, datasources, options):

    def extract_testsuites(suite):

        # Only if the testsuite contains testcases
        if suite.tests:

            # Add the testsuite to the list
            extract_testsuites.list += [suite.source]

        # Continue on child testsuites
        for child in suite.suites:

            extract_testsuites(child)

    extract_testsuites.list = []

    # Parse Robot Framework options in Robot settings
    settings = RobotSettings(options)

    # Create an executable TestSuite object based on existing data on the file system
    # The argument include_suites is the pybot option --suite (see pybot --help)
    suite = TestSuiteBuilder(include_suites=settings['SuiteNames']).build(*datasources)

    # Configure the TestSuite with the remaining suite settings
    suite.configure(**settings.suite_config)

    # Clean the empty suites (without test cases)
    suite.remove_empty_suites()

    # Extract testsuites filenames from the TestSuite object
    extract_testsuites(suite)

    # Put the testsuites list in the queue for the calling process
    queue.put(extract_testsuites.list)


#  Run Robot Framework in a sub process
def sub_run(datasources, options):

    with open(os.devnull, 'w') as devnull:

        # Options for launch Robot in a multi-processing mode
        # ResultsWriter class is used as a listener to write results
        options = options.copy()
        options['suite'] = '*'
        options['log'] = 'NONE'
        options['report'] = 'NONE'
        options['xunit'] = 'NONE'
        options['output'] = 'NONE'
        options['stdout'] = devnull
        options['stderr'] = devnull
        options['consolecolors'] = 'off'
        options['consolemarkers'] = 'off'
        options['listener'] = 'qa_tests.listeners.ResultsWriter'

        # Run Robot Framework on the datasources given in parameters
        run_robot_framework(*datasources, **options)


def main():

    if len(sys.argv) > 1:

        # Get command line options
        options = sys.argv[1:]

        # Default number of processes (cpu count will be used by default)
        number_of_processes = None

        # Try to get '--processes' option from command line
        try:
            # Find '--processes' option index and remove it from options
            index = options.index('--processes')
            options.pop(index)

            # Get '--processes' option value and remove it from options
            number_of_processes = int(options[index])
            options.pop(index)

        except (ValueError, IndexError):
            pass

        try:
            # Parse remaining options with the Robot Framework API
            robot_options, datasources = RobotFramework().parse_arguments(options)

            # Get testsuites list in a sub process
            queue = Queue()
            process = Process(target=sub_get_testsuites, args=(queue, datasources, robot_options))
            process.start()
            testsuites = queue.get()
            process.join()

            if testsuites:

                # Create an output directory
                if os.path.exists("output"):
                    shutil.rmtree("output")
                os.makedirs("output")

                # Create a pool of process
                # Each process receives the Robot Framework native options and a testsuite name by arguments
                pool = Pool(processes=number_of_processes, maxtasksperchild=1)
                processes = [pool.apply_async(sub_run, args=([testsuite], robot_options)) for testsuite in testsuites]
                [process.wait() for process in processes]

            else:
                print "[ \x1b[31mERROR\x1b[0m ] No test suites to execute."

        except Information as information:
            print
            print "A parallel executor for Robot Framework test suites."
            print
            print "Supports all Robot Framework command line options and also following options:"
            print
            print "--processes [NUMBER OF PROCESSES]"
            print "How many parallel executors to use (default is cpu count)"
            print
            print information

        except DataError as error:
            print "[ \x1b[31mERROR\x1b[0m ] {}".format(error)

    else:
        print "[ \x1b[31mERROR\x1b[0m ] Expected at least 1 argument, got 0."
