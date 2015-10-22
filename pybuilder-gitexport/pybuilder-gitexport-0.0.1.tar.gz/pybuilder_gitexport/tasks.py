from pybuilder.core import task, init, depends, use_plugin, description
from pybuilder.errors import BuildFailedException
import os, sys

use_plugin('python.core')

@init
def init_gitexport(project, logger):
  project.depends_on('dulwich')

@task('gitexport')
def gitexport(project, logger):
  from dulwich import porcelain


  targetDir = project.get_property('dir_target')
  url = project.get_property('gitexport_url')

  name = url.split('/')[-1]


  porcelain.clone(url, targetDir + '/' + name)
 
   
