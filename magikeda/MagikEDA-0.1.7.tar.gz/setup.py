from distutils.core import setup

setup(
    name='MagikEDA',
    version='0.1.7',
    author='Saul Campos Berardo',
    author_email='saulberardo@gmail.com',
    packages=['magikeda'],
    scripts=['bin/plot_data_frame_profile.py'],
    url='http://pypi.python.org/pypi/MagikEDA/',
    license='LICENSE',
    description='Scripts to help Exploratory Data Analysis',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas >= 0.15.2",
        "numpy >= 1.9.2",
        "matplotlib >= 1.4.3",
	"basemap >= 1.0.7"
    ],
)

