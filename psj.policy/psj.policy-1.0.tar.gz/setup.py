from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n\n'
    + read('docs', 'SPONSORS.txt')
    + '\n\n'
    + read('docs', 'HISTORY.txt')
    + '\n\n'
    + 'Download\n'
    + '********\n'
    )

tests_require = [
    'plone.app.testing',
    ]

setup(
    name='psj.policy',
    version='1.0',
    author='Uli Fouquet',
    author_email='uli@gnufix.de',
    url='http://pypi.python.org/pypi/psj.policy',
    description='Plone Scholarly Journal - the site policy',
    long_description=long_description,
    license='GPL',
    keywords="zope policy scholarly scholar journal plone plone3 plone4",
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Operating System :: OS Independent',
                 'Framework :: Plone',
                 (
                     "Topic :: Software Development :: Libraries :: "
                     "Python Modules"
                     ),
                 ],
    packages=find_packages(exclude='ez_setup'),
    namespace_packages=['psj'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'grokcore.component',
        'lxml',
        'ulif.openoffice',
        'Plone',
        'Products.Archetypes',
        'restclient',
        ],
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
        },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      [ulif.openoffice.processors]
      psj_html = psj.policy.transforms.processors:PSJHTMLProcessor
      """,
)
