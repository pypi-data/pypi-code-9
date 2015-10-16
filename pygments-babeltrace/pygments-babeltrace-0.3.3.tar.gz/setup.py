from setuptools import setup

setup(
    name="pygments-babeltrace",
    description="Pygments Babeltrace Lexer",
    version="0.3.3",
    url="https://github.com/junousia/pygments-babeltrace",
    download="https://github.com/junousia/pygments-babeltrace/tarball/v0.3.3",
    packages=['pygbab'],
    install_requires=['Pygments'],
    author="Jukka Nousiainen",
    author_email="jukka.nousiainen@gmail.com",

    entry_points={
        'pygments.lexers': ['release = pygbab.babeltrace_lexer:BabeltraceLexer', ]
    }
)
