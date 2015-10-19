from gabbi_html import __version__ as VERSION


META = {
    "name": "gabbi-html",
    "version": VERSION,
    "url": "https://github.com/FND/gabbi-html",
    "author": "FND",
    "packages": ["gabbi_html"],
    "install_requires": ["gabbi", "lxml", "cssselect"],
    "extras_require": {
        "linting": ["pep8"]
    }
}


if __name__ == "__main__":
    from setuptools import setup
    setup(**META)
