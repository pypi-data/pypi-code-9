from setuptools import setup

setup(
    name='boomerang-client',
    version='0.1',
    packages=['boomerang'],
    url='https://github.com/olalidmark/boomerang-client',
    license='MIT',
    author='fantomen',
    author_email='olalidmark@gmail.com',
    description='Boomerang.io Python API client',
    keywords=['boomerang', 'boomerang.io', 'api', 'rest'],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',

    ],
    install_requires=['requests'],
)
