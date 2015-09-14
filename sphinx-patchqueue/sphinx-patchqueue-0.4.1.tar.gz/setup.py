from distutils.core import setup

setup(
    name='sphinx-patchqueue',
    version='0.4.1',
    packages = ['patchqueue'],
    package_data = {'patchqueue': ['static/*']},
    url='https://bitbucket.org/masklinn/sphinx-patchqueue',
    license='BSD',
    author='Xavier Morel',
    author_email='xavier.morel@masklinn.net',
    requires=['sphinx', 'mercurial (<3.4)'],
    description="Sphinx extension for embedding sequences of file alterations",
)
