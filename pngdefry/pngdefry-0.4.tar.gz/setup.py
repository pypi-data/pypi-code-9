import os
from setuptools import setup, Extension, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README")).read()

setup(
    name='pngdefry',
    version=0.4,
    description="Remove iPhone specific optimizations from PNG files",
    author='Piotr Duda Applause',
    author_email='pduda@applause.com',
    url='https://github.com/ApplauseAQI/pngdefry',
    long_description=README,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    license='MIT',
    install_requries=["argparse==1.3.0"],
    ext_modules=[
        Extension(
            '_pngdefry', [
                'src/pngdefry/pngdefry.c',
                'src/pngdefry/miniz.c',
            ],
            extra_compile_args=['-Wno-unused-value -Isrc/pngdefry/'],
        )],
    entry_points={
        "console_scripts": ["pngdefry=pngdefry:main"]
    }
)
