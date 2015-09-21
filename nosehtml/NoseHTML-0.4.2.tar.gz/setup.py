from setuptools import setup, find_packages

setup( name="NoseHTML",
       version="0.4.2",
       description="""HTML Output plugin for Nose / Nosetests""",
       url='https://bitbucket.org/james_taylor/nosehtml/',
       author='James Taylor, Nate Coraor, Dave Bouvier',
       license='MIT',
       packages=['nosehtml'],
       entry_points = {'nose.plugins.0.10': [ 'nosehtml = nosehtml.plugin:NoseHTML' ] }
)
