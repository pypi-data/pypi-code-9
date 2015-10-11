from setuptools import setup
setup(name="dbff",
      version="1.4.1",
      author="Xiayi Li",
      author_email="hi@xiayi.li",
      url="https://github.com/yosg/dbff",
      description="Compare tables and rows between MySQL databases.",
      license="MIT License",
      install_requires=["MySQL-python"],
      py_modules=["comparer"])
