# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('epoca_crawler/epoca_crawler.py').read(),
    re.M
    ).group(1)
 
 
with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "epoca_crawler",
    packages = ["epoca_crawler"],
    entry_points = {
        "console_scripts": ['epoca_crawler = epoca_crawler.epoca_crawler:main']
        },
    version = version,
    description = "Ferramenta para extraçao de informaçoes do site epocacosmeticos.com.br.",
    long_description = long_descr,
    author = "Paulo Cesar G. Sant'Anna",
    author_email = "paulo.santanna89@gmail.com",
    url = "https://github.com/PauloSm/Epoca_Crawler",
    )
