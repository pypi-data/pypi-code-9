from distutils.core import setup

setup(
    name='lambdaJSON',
    version='4.3',
    author='Pooya Eghbali',
    author_email='persian.writer@gmail.com',
    packages=['lambdaJSON'],
    url='https://github.com/pooya-eghbali/lambdaJSON',
    license='LGPLv3',
    description="""Use json to serialize unsupported python types (and many more including functions, classes, exceptions, etc). [stable-py2-py3].""",
    long_description=open('README.txt').read(),
    classifiers= ['Intended Audience :: Developers',
                  'Development Status :: 5 - Production/Stable',
                  'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 3',
                  'Topic :: Software Development :: Libraries :: Python Modules',
                  'Topic :: Utilities'],
    keywords = 'json, serialization, serialize, pickle, marshal',
    platforms= ['Any']
)
