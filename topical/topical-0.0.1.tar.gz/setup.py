import setuptools

setuptools.setup(
    name="topical",
    version="0.0.1",
    author="Tom Leach",
    author_email="tom@gc.com",
    description="Topic-oriented API for producing and consuming Kafka streams with support for pluggable codecs",
    license="MIT",
    keywords="kafka topic encoding decoding streams python",
    url="http://github.com/gamechanger/topical",
    packages=["topical"],
    install_requires=[],
    tests_require=['nose', 'mock']
    )
