from distutils.core import setup

setup(name="quickplots",
      version="0.0.1",
      description="Matplotlib wrapper",
      long_description="An object-oriented wrapper for the powerful matplotlib library.",
      url="https://github.com/samirelanduk/quickplots",
      author="Sam Ireland",
      author_email="sam.ireland.uk@gmail.com",
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3"],
      py_modules=["quickplotss"],
      install_requires=["matplotlib"])
