from distutils.core import setup
setup(
    name = "PyDDIY",
    packages = ["PyDDIY"],
    version = "0.4.2.1",
    description = "IronPython DDIY.dll wrapper.",
    author = "Tomas Bosek",
    author_email = "bosektom@gmail.com",
    url = "https://github.com/Bosek/PyDDIY",
    download_url = "https://github.com/Bosek/PyDDIY",
    keywords = ["image processing", "user input", "ironpython", "automatization"],
    classifiers = [
            "Development Status :: 3 - Alpha",
            "Environment :: Win32 (MS Windows)",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: C#",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: Implementation :: IronPython",
        ],
    long_description = """
PyDDIY is IronPython 2.7 wrapper module for C# library DDIY.
Currently only IronPython 2.7 & Windows support.

DDIY Project can be found at: [DDIY](https://github.com/Bosek/DDIY)
PyDDIY at: [PyDDIY](https://github.com/Bosek/PyDDIY)

-----------------------------------------

Features:
 - Simulates user keyboard and mouse input
 - Basic clipboard text handling(set and get)
 - A few simple WinAPI calls(focus window, get window rectangle)
 - Image processing: can find image template in image / on screen

-----------------------------------------

Since it is very easy to use, I won't write any documentation ATM. Just see docstrings(you can use pydoc) in
each file(there are a few files).
"""
)
