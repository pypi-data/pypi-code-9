from setuptools import setup, find_packages

setup(
    name = "Sherbet",
    version = "0.1",
    description = "Sherbet library introduces smart string formatting",
    url = "https://github.com/vasili-v/sherbet",
    author = "Vasili Vasilyeu",
    author_email = "vasili.v@tut.by",
    license = "MIT",
    long_description = "The library automatically fills specifically named " \
                       "fields in string template. For example: " \
                       "format(\"{length:d} file{length_suffix} " \
                       "{length_option<has|have>} been deleted\", length=5) " \
                       "returns \"5 files have been deleted\".",
    platforms = ["Darwin", "Linux"],
    py_modules = ['sherbet'],
    test_suite = "test.all"
)
