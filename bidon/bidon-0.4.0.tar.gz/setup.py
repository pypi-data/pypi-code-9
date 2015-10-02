from setuptools import setup, find_packages

version = "0.4.0"

setup(name="bidon",
      version=version,
      license="BSD",
      platforms="any",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      packages=find_packages(),
      description="A simple, easy to use, and flexible data handling library",
      url="https://github.com/treycucco/bidon",
      download_url="https://github.com/treycucco/bidon/tarball/master",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only"
      ])
