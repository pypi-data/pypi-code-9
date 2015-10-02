from setuptools import setup, find_packages

setup(
    name='snakespec',
    version='0.1.2',
    description='BDD testing for python',
    long_description='A simple, scale-free BDD testing plugin for Python',
    url='https://github.com/iredelmeier/snakespec',
    author='Isobel Redelmeier',
    author_email='iredelmeier@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    keywords='test nosetests nose nosetest tdd bdd testing rspec',
    packages=find_packages(exclude=['test', 'docs']),
    install_requires=['nose'],
    entry_points={'nose.plugins.0.10': ['snakespec=snakespec.snakespec:SnakeSpec']},
)
