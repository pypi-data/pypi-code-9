USAGE = """\
Robot Framework -- A generic test automation framework

Usage:  pybot|jybot|ipybot [options] data_sources
   or:  python|jython|ipy -m robot.run [options] data_sources
   or:  python|jython|ipy path/to/robot/run.py [options] data_sources
   or:  java -jar robotframework.jar run [options] data_sources

Robot Framework is a Python-based keyword-driven test automation framework for
acceptance level testing and acceptance test-driven development (ATDD). It has
an easy-to-use tabular syntax for creating test cases and its testing
capabilities can be extended by test libraries implemented either with Python
or Java. Users can also create new keywords from existing ones using the same
simple syntax that is used for creating test cases.

Depending is Robot Framework installed using Python, Jython, or IronPython
interpreter, it has a start-up script, `pybot`, `jybot` or `ipybot`,
respectively. Alternatively, it is possible to directly execute `robot.run`
module (e.g. `python -m robot.run`) or `robot/run.py` script using a selected
interpreter. Finally, there is also a standalone JAR distribution.

Data sources given to Robot Framework are either test case files or directories
containing them and/or other directories. Single test case file creates a test
suite containing all the test cases in it and a directory containing test case
files creates a higher level test suite with test case files or other
directories as sub test suites. If multiple data sources are given, a virtual
top level suite containing suites generated from given data sources is created.

By default Robot Framework creates an XML output file and a log and a report in
HTML format, but this can be configured using various options listed below.
Outputs in HTML format are for human consumption and XML output for integration
with other systems. XML outputs can also be combined and otherwise further
processed with `rebot` tool. Run `rebot --help` for more information.

Robot Framework is open source software released under Apache License 2.0.
Its copyrights are owned and development supported by Nokia Siemens Networks.
For more information about the framework see http://robotframework.org.

Options
=======

 -N --name name           Set the name of the top level test suite. Underscores
                          in the name are converted to spaces. Default name is
                          created from the name of the executed data source.
 -D --doc documentation   Set the documentation of the top level test suite.
                          Underscores in the documentation are converted to
                          spaces and it may also contain simple HTML formatting
                          (e.g. *bold* and http://url/).
 -M --metadata name:value *  Set metadata of the top level test suite.
                          Underscores in the name and value are converted to
                          spaces. Value can contain same HTML formatting as
                          --doc. Example: `--metadata version:1.2`
 -G --settag tag *        Sets given tag(s) to all executed test cases.
 -t --test name *         Select test cases to run by name or long name. Name
                          is case and space insensitive and it can also be a
                          simple pattern where `*` matches anything and `?`
                          matches any char. If using `*` and `?` in the console
                          is problematic see --escape and --argumentfile.
 -s --suite name *        Select test suites to run by name. When this option
                          is used with --test, --include or --exclude, only
                          test cases in matching suites and also matching other
                          filtering criteria are selected. Name can be a simple
                          pattern similarly as with --test and it can contain
                          parent name separated with a dot. For example
                          `-s X.Y` selects suite `Y` only if its parent is `X`.
 -i --include tag *       Select test cases to run by tag. Similarly as name in
                          --test, tag is case and space insensitive. There are
                          three ways to include test based on tags:
                          1) One tag as a simple pattern. Tests having a tag
                          matching the pattern are included. Example: `it-*`
                          2) Two or more tags (or patterns) separated by `&` or
                          `AND`. Only tests having all these tags are included.
                          Examples: `tag1&tag2`, `smokeANDowner-*ANDit-10`
                          3) Two or more tags (or patterns) separated by `NOT`.
                          Tests having the first tag but not any of the latter
                          ones are included. Example: `it-10NOTsmoke`
 -e --exclude tag *       Select test cases not to run by tag. These tests are
                          not run even if they are included with --include.
                          Tags are excluded using the rules explained in
                          --include.
 -R --runfailed output    Select failed tests from an earlier output file to be
                          re-executed. Equivalent to selecting same tests
                          individually using --test option.
 -c --critical tag *      Tests having given tag are considered critical. If no
                          critical tags are set, all tags are critical. Tags
                          can be given as a pattern like e.g. with --test.
 -n --noncritical tag *   Tests with given tag are not critical even if they
                          have a tag set with --critical. Tag can be a pattern.
 -v --variable name:value *  Set variables in the test data. Only scalar
                          variables are supported and name is given without
                          `${}`. See --escape for how to use special characters
                          and --variablefile for a more powerful variable
                          setting mechanism that allows also list variables.
                          Examples:
                          --variable str:Hello  =>  ${str} = `Hello`
                          -v str:Hi_World -E space:_  =>  ${str} = `Hi World`
                          -v x: -v y:42  =>  ${x} = ``, ${y} = `42`
 -V --variablefile path *  File to read variables from (e.g. `path/vars.py`).
                          Example file:
                          |  import random
                          |  __all__ = [`scalar`, `LIST__var`, `integer`]
                          |  scalar = `Hello world!`
                          |  LIST__var = [`Hello`, `list`, `world`]
                          |  integer = random.randint(1,10)
                          =>
                          ${scalar} = `Hello world!`
                          @{var} = [`Hello`,`list`,`world`]
                          ${integer} = <random integer from 1 to 10>
 -d --outputdir dir       Where to create output files. The default is the
                          directory where tests are run from and the given path
                          is considered relative to that unless it is absolute.
 -o --output file         XML output file. Given path, similarly as paths given
                          to --log, --report, --xunit, and --debugfile, is
                          relative to --outputdir unless given as an absolute
                          path. Other output files are created based on XML
                          output files after the test execution and XML outputs
                          can also be further processed with Rebot tool. Can be
                          disabled by giving a special value `NONE`. In this
                          case, also log and report are automatically disabled.
                          Default: output.xml
 -l --log file            HTML log file. Can be disabled by giving a special
                          value `NONE`. Default: log.html
                          Examples: `--log mylog.html`, `-l NONE`
 -r --report file         HTML report file. Can be disabled with `NONE`
                          similarly as --log. Default: report.html
 -x --xunit file          xUnit compatible result file. Not created unless this
                          option is specified.
    --xunitfile file      Deprecated. Use --xunit instead.
    --xunitskipnoncritical  Mark non-critical tests on xUnit output as skipped.
 -b --debugfile file      Debug file written during execution. Not created
                          unless this option is specified.
 -T --timestampoutputs    When this option is used, timestamp in a format
                          `YYYYMMDD-hhmmss` is added to all generated output
                          files between their basename and extension. For
                          example `-T -o output.xml -r report.html -l none`
                          creates files like `output-20070503-154410.xml` and
                          `report-20070503-154410.html`.
    --splitlog            Split log file into smaller pieces that open in
                          browser transparently.
    --logtitle title      Title for the generated test log. The default title
                          is `<Name Of The Suite> Test Log`. Underscores in
                          the title are converted into spaces in all titles.
    --reporttitle title   Title for the generated test report. The default
                          title is `<Name Of The Suite> Test Report`.
    --reportbackground colors  Background colors to use in the report file.
                          Either `all_passed:critical_passed:failed` or
                          `passed:failed`. Both color names and codes work.
                          Examples: --reportbackground green:yellow:red
                                    --reportbackground #00E:#E00
 -L --loglevel level      Threshold level for logging. Available levels: TRACE,
                          DEBUG, INFO (default), WARN, NONE (no logging). Use
                          syntax `LOGLEVEL:DEFAULT` to define the default
                          visible log level in log files.
                          Examples: --loglevel DEBUG
                                    --loglevel DEBUG:INFO
    --suitestatlevel level  How many levels to show in `Statistics by Suite`
                          in log and report. By default all suite levels are
                          shown. Example:  --suitestatlevel 3
    --tagstatinclude tag *  Include only matching tags in `Statistics by Tag`
                          and `Test Details` in log and report. By default all
                          tags set in test cases are shown. Given `tag` can
                          also be a simple pattern (see e.g. --test).
    --tagstatexclude tag *  Exclude matching tags from `Statistics by Tag` and
                          `Test Details`. This option can be used with
                          --tagstatinclude similarly as --exclude is used with
                          --include.
    --tagstatcombine tags:name *  Create combined statistics based on tags.
                          These statistics are added into `Statistics by Tag`
                          and matching tests into `Test Details`. If optional
                          `name` is not given, name of the combined tag is got
                          from the specified tags. Tags are combined using the
                          rules explained in --include.
                          Examples: --tagstatcombine tag1ANDtag2:My_name
                                    --tagstatcombine requirement-*
    --tagdoc pattern:doc *  Add documentation to tags matching given pattern.
                          Documentation is shown in `Test Details` and also as
                          a tooltip in `Statistics by Tag`. Pattern can contain
                          characters `*` (matches anything) and `?` (matches
                          any char). Documentation can contain formatting
                          similarly as with --doc option.
                          Examples: --tagdoc mytag:My_documentation
                                    --tagdoc regression:*See*_http://info.html
                                    --tagdoc owner-*:Original_author
    --tagstatlink pattern:link:title *  Add external links into `Statistics by
                          Tag`. Pattern can contain characters `*` (matches
                          anything) and `?` (matches any char). Characters
                          matching to wildcard expressions can be used in link
                          and title with syntax %N, where N is index of the
                          match (starting from 1). In title underscores are
                          automatically converted to spaces.
                          Examples: --tagstatlink mytag:http://my.domain:Link
                          --tagstatlink bug-*:http://tracker/id=%1:Bug_Tracker
    --removekeywords all|passed|for|wuks|name:<pattern> *  Remove keyword data
                          from the generated log file. Keywords containing
                          warnings are not removed except in `all` mode.
                          all:            remove data from all keywords
                          passed:         remove data only from keywords in
                                          passed test cases and suites
                          for:            remove passed iterations from for
                                          loops
                          wuks:           remove all but last failing keyword
                                          from `Wait Until Keyword Succeeds`
                          name:<pattern>: remove those keywords that matches
                                          pattern. Pattern can be the full name
                                          of the keyword with spaces removed or
                                          `*` wildcard.
    --listener class *    A class for monitoring test execution. Gets
                          notifications e.g. when a test case starts and ends.
                          Arguments to listener class can be given after class
                          name, using colon as separator. For example:
                          --listener MyListenerClass:arg1:arg2
    --warnonskippedfiles  If this option is used, skipped files will cause a
                          warning that is visible to console output and log
                          files. By default skipped files only cause an info
                          level syslog message.
    --nostatusrc          Sets the return code to zero regardless of failures
                          in test cases. Error codes are returned normally.
    --runemptysuite       Executes tests also if the top level test suite is
                          empty. Useful e.g. with --include/--exclude when it
                          is not an error that no test matches the condition.
    --dryrun              Verifies test data and runs tests so that library
                          keywords are not executed.
    --exitonfailure       Stops test execution if ant critical test fails.
    --skipteardownonexit  Causes teardowns to be skipped if test execution is
                          stopped prematurely.
    --randomize all|suites|tests|none  Randomizes the test execution order.
                          all:    randomizes both suites and tests
                          suites: randomizes suites
                          tests:  randomizes tests
                          none:   no randomization (default)
    --runmode mode *      Deprecated in version 2.8. Use individual options
                          --dryrun, --exitonfailure, --skipteardownonexit, or
                          --randomize instead.
 -W --monitorwidth chars  Width of the monitor output. Default is 78.
 -C --monitorcolors auto|on|ansi|off  Use colors on console output or not.
                          auto: use colors when output not redirected (default)
                          on:   always use colors
                          ansi: like `on` but use ANSI colors also on Windows
                          off:  disable colors altogether
                          Note that colors do not work with Jython on Windows.
 -K --monitormarkers auto|on|off  Show `.` (success) or `F` (failure) on
                          console when top level keywords in test cases end.
                          Values have same semantics as with --monitorcolors.
 -P --pythonpath path *   Additional locations (directories, ZIPs, JARs) where
                          to search test libraries from when they are imported.
                          Multiple paths can be given by separating them with a
                          colon (`:`) or using this option several times. Given
                          path can also be a glob pattern matching multiple
                          paths but then it normally must be escaped or quoted.
                          Examples:
                          --pythonpath libs/
                          --pythonpath /opt/testlibs:mylibs.zip:yourlibs
                          -E star:STAR -P lib/STAR.jar -P mylib.jar
 -E --escape what:with *  Escape characters which are problematic in console.
                          `what` is the name of the character to escape and
                          `with` is the string to escape it with. Note that
                          all given arguments, incl. data sources, are escaped
                          so escape characters ought to be selected carefully.
                          Available escapes: amp (&), apos ('), at (@), bslash
                          (\), colon (:), comma (,), curly1 ({), curly2 (}),
                          dollar ($), exclam (!), gt (>), hash (#), lt (<),
                          paren1 ((), paren2 ()), percent (%), pipe (|), quest
                          (?), quot ("), semic (;), slash (/), space ( ),
                          square1 ([), square2 (]), star (*)
                          Examples:
                          --escape space:_ --metadata X:Value_with_spaces
                          -E space:SP -E quot:Q -v var:QhelloSPworldQ
 -A --argumentfile path *  Text file to read more arguments from. Use special
                          path `STDIN` to read contents from the standard input
                          stream. File can have both options and data sources
                          one per line. Contents do not need to be escaped but
                          spaces in the beginning and end of lines are removed.
                          Empty lines and lines starting with a hash character
                          (#) are ignored.
                          Example file:
                          |  --include regression
                          |  --name Regression Tests
                          |  # This is a comment line
                          |  my_tests.html
                          |  path/to/test/directory/
                          Examples:
                          --argumentfile argfile.txt --argumentfile STDIN
 -h -? --help             Print usage instructions.
 --version                Print version information.

Options that are marked with an asterisk (*) can be specified multiple times.
For example, `--test first --test third` selects test cases with name `first`
and `third`. If other options are given multiple times, the last value is used.

Long option format is case-insensitive. For example, --SuiteStatLevel is
equivalent to but easier to read than --suitestatlevel. Long options can
also be shortened as long as they are unique. For example, `--logti Title`
works while `--lo log.html` does not because the former matches only --logtitle
but the latter matches --log, --loglevel and --logtitle.

Environment Variables
=====================

ROBOT_SYSLOG_FILE         Path to a file where Robot Framework writes internal
                          information about parsing test case files and running
                          tests. Can be useful when debugging problems. If not
                          set, or set to special value `NONE`, writing to the
                          syslog file is disabled.
ROBOT_SYSLOG_LEVEL        Log level to use when writing to the syslog file.
                          Available levels are the same as for --loglevel
                          command line option and the default is INFO.

Examples
========

# Simple test run with `pybot` without options.
$ pybot tests.html

# Using options and running with `jybot`.
$ jybot --include smoke --name Smoke_Tests path/to/tests.txt

# Executing `robot.run` module using Python.
$ python -m robot.run --test test1 --test test2 test_directory

# Running `robot/run.py` script with Jython.
$ jython /path/to/robot/run.py tests.robot

# Executing multiple test case files and using case-insensitive long options.
$ pybot --SuiteStatLevel 2 /my/tests/*.html /your/tests.html

# Setting syslog file before running tests.
$ export ROBOT_SYSLOG_FILE=/tmp/syslog.txt
$ pybot tests.tsv
"""