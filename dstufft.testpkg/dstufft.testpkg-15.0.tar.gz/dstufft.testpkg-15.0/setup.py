import setuptools


setuptools.setup(
    name="dstufft.testpkg",
    version="15.0",
    requires=["foo"],
    provides=["bar"],
    obsoletes=["lol"],
    install_requires=["requests"],
    py_modules=["f"],
)
