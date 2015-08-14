from distutils.core import setup

setup(
    name="nicosearch",
    py_modules=['nicosearch'],
    version="0.2.0",
    license='MIT License',
    download_url="https://github.com/ymizushi/nicosearch/archive/master.zip",
    platforms=['POSIX'],
    description="https://github.com/ymizushi/nicosearch",
    author="ymizushi",
    author_email="mizushi@gmail.com",
    url="https://github.com/ymizushi/nicosearch",
    keywords=["search", "niconico", "library"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Software Development",
    ],
    install_requires=[
        'requests>=2.2.1',
    ],
    long_description="nicosearch is a searching library for niconico platform. nicosearch wraps niconico search API. See http://search.nicovideo.jp/docs/api/snapshot.html ."
)
