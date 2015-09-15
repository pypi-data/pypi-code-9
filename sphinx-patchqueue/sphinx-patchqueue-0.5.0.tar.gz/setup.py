from distutils.core import setup

setup(
    name='sphinx-patchqueue',
    version='0.5.0',
    packages = ['patchqueue'],
    package_data = {'patchqueue': ['static/*']},
    url='https://bitbucket.org/masklinn/sphinx-patchqueue',
    license='BSD',
    author='Xavier Morel',
    author_email='xavier.morel@masklinn.net',
    requires=['sphinx', 'mercurial (<3.6)'],
    description="Sphinx extension for embedding sequences of file alterations",
)
