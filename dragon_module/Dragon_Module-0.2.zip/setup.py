#remember, if you want to bundle a module with this that isn't automatically installed with Python,
#then put it under install_requires.
#Designed for Python 2.7.10.
from distutils.core import setup

setup(

    #name
    name = "Dragon_Module",
    #version
    version = "0.2",
    #description
    description = "A module that improves the functionality of Python 2.7.10. All rights reserved.",
    #url
    url = "http://legendiaservers.wix.com/dragon",
    #requirements
    install_requires = ["easygui"],
    #author
    author = "Dragon.net Servers",
    #author_email
    author_email = "Dragon.net@usa.com",
    #packages
    py_modules = ["dragon"],
)