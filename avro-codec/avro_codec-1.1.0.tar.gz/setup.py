import setuptools


setuptools.setup(
    name="avro_codec",
    version="1.1.0",
    author="Tom Leach",
    author_email="tom@gc.com",
    description="An avro codec which exposes an API similar to the standard library's marshal, pickle and json modules",
    license="MIT",
    keywords="avro encode decode codec",
    url="http://github.com/gamechanger/avro_codec",
    packages=["avro_codec"],
    long_description="",
    install_requires=['avro==1.7.7', 'fastavro==0.9.5'],
    tests_require=['nose']
)
