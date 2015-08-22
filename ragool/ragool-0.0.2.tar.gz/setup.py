from setuptools import setup


setup(name="ragool",
      version="0.0.2",
      description="Handle Bottle.py errors with love <3",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Framework :: Bottle",
        "Topic :: Utilities",
      ],
      keywords="error handling",
      url="https://github.com/aybb/ragool",
      author="aybb",
      author_email="lasthitknxx@gmail.com",
      license="MIT",
      packages=["Ragool"],
      install_requires=[
          "bottle"
      ],
      include_package_data=True,
      zip_safe=False)