import setuptools
import base64


def read(f):
    with open(f) as h:
        return h.read()


setuptools.setup(
    name='photonemitter',
    version=read('photonemitter/version'),
    packages=setuptools.find_packages(),
    author='lf',
    author_email=base64.b64decode(b'cH10aG9uQGxmY29kZS5jYQ==').decode(),
    description='A simple search backend system currently designed for '
                'lighthouse',
    long_description=read('README.rst'),
    license='MIT',
    url='https://github.com/lf-/photonemitter',
    keywords=['lighthouse', 'search'],

    entry_points={
        'console_scripts': [
            'photonemitter = photonemitter.__main__:main'
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities'
    ]
)
