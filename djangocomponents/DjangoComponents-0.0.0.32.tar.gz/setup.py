from setuptools import setup, find_packages

setup(
    name='DjangoComponents',
    version='0.0.0.32',
    description='Package of reusable Django components',
    long_description='',
    url='',
    author='Lightning Kite',
    author_email='',
    license='',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='django components reusable',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    package_data={
        # any additional data files
    },
    data_files=[],
    entry_points={
        # entry points - console_scripts?
    },
)
