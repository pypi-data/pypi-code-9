from setuptools import setup, find_packages

setup(
    name = 'pynoise',
    packages = find_packages(),
    include_package_data=True,
    platforms='any',
    version = '2.1.0a4',
    description = 'An implementation of libnoise in python. Allows the creation of verious noise maps using a series of interconnected noise modules.',
    author = 'Tim Butram',
    author_email = 'tim@timchi.me',
    url = 'https://gitlab.com/atrus6/pynoise',
    download_url = 'https://gitlab.com/atrus6/pynoise/repository/archive.tar.gz',
    keywords = ['perlin', 'noise', 'procedural'],
    install_requires = ['sortedcontainers>=0.9.6', 'colormath', 'pillow', 'numpy', 'pyopencl']
)
