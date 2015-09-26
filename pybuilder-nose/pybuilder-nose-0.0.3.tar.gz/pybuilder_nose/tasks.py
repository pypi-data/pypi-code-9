from pybuilder.core import task, init, depends, use_plugin, description
from pybuilder.errors import BuildFailedException
import os, sys, subprocess
from pybuilder_nose.utils import getImportantDirs
from pybuilder_nose.utils import prepareArgs

use_plugin('python.core')

@init
def init_nose(project, logger):
  project.build_depends_on('nose')
  project.build_depends_on('coverage')

@task('run_unit_tests')
@description('Run your entire test suite with Node')
@depends('prepare')
def run_unit_tests(project, logger):

  # set cwd to project root
  src_dir, test_dir, html_dir, xml_file, xunit_file = getImportantDirs(project)

  logger.debug("SRC dir: %s" % src_dir)
  logger.debug("Test dir: %s" % test_dir)
  logger.debug("HTML Reports dir: %s" % html_dir)
  logger.debug("XML Report: %s" % xml_file)
  logger.debug("Xunit Report: %s" % xunit_file) 

  if os.path.exists(html_dir) == False:
    os.makedirs(html_dir)

  logger.debug("Setting initial nose properties")

  project.set_property('nose_where', test_dir)
  project.set_property('nose_cover-package', 'src/main/python')
  project.set_property('nose_with-coverage', True)
  project.set_property('nose_cover-xml', True)
  project.set_property('nose_cover-xml-file', xml_file)
  project.set_property('nose_cover-html', True)
  project.set_property('nose_cover-html-dir', html_dir)
  project.set_property('nose_with-xunit', True)
  project.set_property('nose_xunit-file', xunit_file)

  if project.get_property('verbose'):
    project.set_property('nose_nocapture', True)
    project.set_property('verbose', True)

  logger.debug("Collecting nose properties")

  args = ['nosetest']

  args = prepareArgs(project)
  args.insert(0, 'nosetests')

  for arg in args:
    logger.debug('Nose arg: %s' % arg)

  noseEnv = os.environ.copy()
  noseEnv["PYTHONPATH"] = "src/main/python"

  logger.info("Launching nosetests")
  noseProc = subprocess.Popen(args, stdout=subprocess.PIPE, env=noseEnv)

  while noseProc.poll() is None:
    l = noseProc.stdout.readline()
    logger.debug(l)

  if noseProc.returncode != 0:
    logger.error('Unit tests failed with exit code %s' % noseProc.returncode)
    raise BuildFailedException('Unit tests did not pass')


@depends('run_unit_tests')
@task
def analyze(project, logger):
  logger.debug("ANALYZE TASK")
  pass

@task('clean')
def clean_coverage(project, logger):
  
  coverage_file = ".coverage"

  if os.path.exists(coverage_file):
    logger.debug("Removing %s" % coverage_file)
    os.remove(coverage_file)


