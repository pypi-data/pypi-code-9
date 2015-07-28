from setuptools import setup, find_packages

try:
    desc = open('README.rst').read()
except:
    desc = 'see README.rst'

setup(
    name='nose-printlog',
    version='0.1.0',
    description='Pring log to console in nose tests',
    long_description=desc,
    author='Fumihiro Bessho',
    author_email='fumihiro.bessho@gmail.com',
    url='http://github.com/fbessho/nose-printlog/',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['nose'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'nose.plugins': ['printlog = noseprintlog.noseprintlog:PrintLog']
    },
)
