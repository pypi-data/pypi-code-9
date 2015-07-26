from distutils.core import setup

setup(
    name='pybridge',
    version='1.0.0',
    author='Pooya Eghbali',
    author_email='persian.writer@gmail.com',
    packages=['pybridge'],
    url='https://github.com/pooya-eghbali/bridge',
    description="""Bridge for Python (Bridge is a light-weight portable Natural Language Processing Library)""",
    long_description=open('README.txt').read(),
    classifiers= ['Intended Audience :: Developers',
                  'Development Status :: 5 - Production/Stable',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 3',
                  'Topic :: Software Development :: Libraries :: Python Modules'],
    keywords = 'natural language processing, nlp',
    platforms= ['Any']
)
