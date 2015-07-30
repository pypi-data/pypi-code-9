from setuptools import setup, find_packages

setup(
    name = "pysentosa",
    version="0.1.1",
    packages = find_packages(),
    data_files=[('pysentosa', ['pysentosa/pymerlion.so'])],
    description = "Sentosa - An automatic algorithmic trading system",
    long_description="Python API for sentosa trading system",
    author = "Wu Fuheng",
    author_email = "wufuheng@gmail.com",

    license = "GPL",
    keywords = ("sentosa", "python"),
    platforms = "Independant",
    url = "http://www.quant365.com",
)
