from setuptools import setup, find_packages

setup(
    name = "Sherbet",
    version = "0.1.1",
    description = "Sherbet library automates word inflection to support plurals",
    url = "https://github.com/vasili-v/sherbet",
    author = "Vasili Vasilyeu",
    author_email = "vasili.v@tut.by",
    license = "MIT",
    long_description = "The library is a superset for curly braces " \
                       "formatting. Any format suitable for str.format also " \
                       "works for sherbet. Additionally the library " \
                       "supports automatic plural froms. For example string " \
                       "\"{x} file{x_plural} {x_plural<are|is>} here.\" " \
                       "is formatted to \"1 file is here.\" if x is 1 " \
                       "and to \"5 files are here\" if x is 5. Currently " \
                       "only english is supported.",
    platforms = ["Darwin", "Linux"],
    py_modules = ['sherbet'],
    test_suite = "test"
)
