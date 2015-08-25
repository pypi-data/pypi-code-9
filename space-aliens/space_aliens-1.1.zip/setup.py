from setuptools import setup, find_packages

with open("README.rst", encoding="utf8") as file:
    long_description = file.read()

setup(
      name="space_aliens",
      version="1.1",
      description="top-down space shooter",
      long_description=long_description,
      url="http://semicoded.com/",
      author="semicoded",
      author_email="admin@semicoded.com",
      license="BSD 2-Clause License",
      classifiers=[
                   "Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: End Users/Desktop",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: Microsoft :: Windows",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.4",
                   "Topic :: Games/Entertainment",
                   "Topic :: Games/Entertainment :: Arcade"
                   ],
      keywords="game space aliens arcade shooter",
      packages=find_packages(),
      install_requires=["pygame"],
      include_package_data = True # specified in MANIFEST.in
)