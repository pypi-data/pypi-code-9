# -*-coding:utf-8-*-


from setuptools import setup


setup(
    name='rsyncrun',
    version='1.1.1',
    url='http://github.com/17zuoye/rsyncrun/',
    license='MIT',
    author='David Chen',
    author_email=''.join(reversed("moc.liamg@emojvm")),
    description='Rsync your code to server and run.',
    long_description=open("README.md").read(),
    packages=["rsyncrun"],
    scripts=[
        'bin/rsyncrun',
    ],

    zip_safe=False,
    platforms='any',
    install_requires=[
        'cached_property',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
