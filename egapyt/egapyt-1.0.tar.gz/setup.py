from setuptools import setup, find_packages
setup(
  name="egapyt",
  version=1.0,
  packages=["ega"],
  install_requires=[
    "docopt",
  ],
  entry_points={
    "console_scripts": [
      "ega=ega.egapyt:cmd"
    ]
  }
)
