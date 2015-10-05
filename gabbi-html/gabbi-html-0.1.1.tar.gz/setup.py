META = {
    "name": "gabbi-html",
    "version": "0.1.1", # TODO: move into package
    "url": "https://github.com/FND/gabbi-html",
    "author": "FND",
    "py_modules": ["gabbi_html"],
    "install_requires": ["gabbi", "lxml", "cssselect"],
    "extras_require": {
        "linting": ["pep8"]
    }
}


if __name__ == "__main__":
    from setuptools import setup
    setup(**META)
