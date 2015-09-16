from setuptools import setup, find_packages

version = "0.3.2"

setup(name="pxp",
      version=version,
      license="BSD",
      platforms="any",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      packages=find_packages(exclude=["config", "tests"]),
      description="A simple python-hosted expression language.",
      url="https://github.com/treycucco/pxp",
      download_url="https://github.com/treycucco/pxp/tarball/master",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4"
      ],
      install_requires=["pyebnf>=0.1.1"])
