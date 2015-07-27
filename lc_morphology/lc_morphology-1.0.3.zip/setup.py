from distutils.core import setup

setup(
    name='lc_morphology',
    version='1.0.3',
    py_modules=['morphology'],
    packages=['lc_morphology'],
    package_data={'lc_morphology': ['data/*.txt']},
    install_requires=['nltk'],
    author='Leonty Chudinov',
    author_email='leonty@inbox.ru',
    url='http://cleonty.ru',
    description='This is a morphology package for Russian language'
)
