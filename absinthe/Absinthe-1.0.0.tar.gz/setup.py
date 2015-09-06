from setuptools import setup, find_packages

setup(
    name = "Absinthe",
    version = '1.0.0',
    description = "A tiny server(-client) app to open sshfs connected files over ssh in any local editor",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/absinthe',
    license = 'MIT',
    install_requires = [
        "gevent-websocket==0.9.3",
        "python-jsonrpc==0.7.12",
    ],
    packages = find_packages(),
    include_package_data = True,
    scripts = [
        'bin/absinthe',
        'bin/abs',
    ],
)
