import os

def getImportantDirs(project):
  cwd = os.getcwd()
  html_dir = cwd + "/" + project.expand("$dir_target/reports/coverage_html")
  xml_file = cwd + "/" + project.expand("$dir_target/reports/coverage.xml")
  xunit_file = cwd + "/" + project.expand("$dir_target/reports/coverage.xunit.xml")
  src_dir = cwd + "/" + project.get_property("dir_source_main_python")
  test_dir = cwd + "/" + project.get_property("dir_source_unittest_python", 'src/unittest/python')

  return (src_dir, test_dir, html_dir, xml_file, xunit_file)

def prepareArgs(project):

  args = []

  for propName, propValue in project.properties.iteritems():
    if propName.startswith('nose_'):
      propName = propName.replace('nose_', '')
      
      if isinstance(propValue, (type(None),str,int,float,bool)) or not hasattr(propValue, '__iter__'):
        propValue = [propValue]

      for pv in propValue:
        if pv == True:
          args.append('--' + str(propName))
        elif pv != False and pv != None:
          args.append('--' + propName + '=' + str(pv))
  
  return args

  
