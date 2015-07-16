from setuptools import setup

setup(
    name="spittalpond",
    version="0.1.3",
    description="A Python interface for the OasisLMF Django webservices API.",
    url="https://github.com/beckettsimmons/spittalpond",
    author="Beckett Simmons",
    author_email="beckettsimmons@hotmail.com",
    packages=["spittalpond"],
    install_requires=["requests", "pytoml"],
    zip_safe=False
)
