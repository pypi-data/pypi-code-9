from setuptools import setup, find_packages

install_requires = ['jinja2', 'flask', 'django']

setup(
    name='blocky',
    version='0.0.2',
    description='Block rendering for flask and django using jinja2.',
    long_description='',
    keywords='flask jinja2 django',
    author='Cameron A. Stitt',
    author_email='cameron@cam.st',
    url='https://github.com/OpenPixel/blocky',
    license='BSD',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "docs"]
    ),
    test_suite='tests.runtests.runtests',
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",

        "Topic :: Software Development :: Libraries :: Python Modules",

        "Programming Language :: Python",
    ]
)
