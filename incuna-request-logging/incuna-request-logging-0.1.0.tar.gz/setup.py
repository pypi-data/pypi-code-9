from setuptools import setup


setup(
    name='incuna-request-logging',

    version='0.1.0',

    description='Django request logging',
    url='https://github.com/incuna/incuna-request-logging',
    author='Incuna',
    author_email='admin@incuna.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
    ],

    packages=['logger'],
    setup_requires=['wheel'],
)
