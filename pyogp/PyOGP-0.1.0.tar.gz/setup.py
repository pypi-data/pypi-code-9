from distutils.core import setup

setup(
    name="PyOGP",

    version="0.1.0",

    author="holonnn",
    author_email="rururu0729@gmail.com",

    # Packages
    packages=["pyogp"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/holdonnn/PyOGP/",

    license="LICENSE.txt",
    description="Python Crawler based on Open-Graph Protocol",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[

    ],
)