from setuptools import setup, find_packages

setup(
    name='emencia-cookie-law',
    version=__import__('cookie_law').__version__,
    description=__import__('cookie_law').__doc__,
    long_description=open('README.rst').read(),
    author='Emencia',
    author_email='dthenon@emencia.com',
    url='https://github.com/emencia/emencia-cookie-law',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        "Framework :: Django :: 1.4",
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
    ],
    #entry_points={
        #'console_scripts': [
            #'emencia-cookie-law = cookie_law.console_script:main',
        #]
    #},
    include_package_data=True,
    zip_safe=False
)