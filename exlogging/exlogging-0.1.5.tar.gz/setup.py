import setuptools


def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(
    name='exlogging',
    version='0.1.5',
    packages=['.'],
    description="Supports to setup python standard logging package.",
    long_descriptiondescription=readme(),
    classifiers=[
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    license='MIT',
    author='Motoki Naruse',
    author_email='motoki@naru.se',
    url='https://github.com/narusemotoki/exlogging',
    keywords=' '.join(['log', 'logging', 'logger']),
    zip_safe=False,
    install_requires=[],
    extras_require={
        'test': [
            'nose',
            'rednose',
            'coverage',
            'flake8',
        ],
    }
)
