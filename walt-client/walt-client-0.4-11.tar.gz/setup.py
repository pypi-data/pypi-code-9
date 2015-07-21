from setuptools import setup, find_packages
setup(
    name = "walt-client",
    version = "0.4-11",
    packages = find_packages(),
    install_requires = ['rpyc>=3.3','plumbum>=1.4.2',
                        'walt-common'],

    # metadata for upload to PyPI
    author = "Etienne Duble",
    author_email = "etienne.duble@imag.fr",
    description = "WalT (Wireless Testbed) control tool.",
    license = "LGPL",
    keywords = "WalT wireless testbed",
    url = "http://walt.forge.imag.fr/",

    namespace_packages = ['walt'],
    entry_points = {
        'console_scripts': [
            'walt = walt.client.client:run'
        ]
    },
)

