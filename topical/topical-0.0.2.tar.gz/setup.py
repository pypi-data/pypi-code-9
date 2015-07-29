import setuptools

setuptools.setup(
    name="topical",
    version="0.0.2",
    author="Tom Leach",
    author_email="tom@gc.com",
    description="Topic-oriented API for producing and consuming Kafka streams with support for pluggable codecs",
    license="MIT",
    keywords="kafka topic encoding decoding streams python",
    url="http://github.com/gamechanger/topical",
    packages=["topical"],
    install_requires=['avro_codec==1.0.0'],
    tests_require=['nose', 'mock']
    )
