from distutils.core import setup

setup(
    name='pybridge',
    version='1.0.1',
    author='Pooya Eghbali',
    author_email='persian.writer@gmail.com',
    packages=['pybridge'],
    url='https://github.com/pooya-eghbali/bridge',
    description="""Bridge for Python (Bridge is a light-weight portable Natural Language Processing Library)""",
    long_description=open('README.txt').read(),
    classifiers= [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords = 'natural language processing, nlp',
    platforms= ['Any']
)
