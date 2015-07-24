from setuptools import setup, find_packages


setup(
    name="my_shiny_converter",
    version="0.2",
    install_requires=[
        'pandas',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'id_concat = converter.converter:main',
        ]
    }
)
