from setuptools import setup, find_packages

setup(
    name='pyair',
    version='3.0.0',
    packages=find_packages(exclude=['docs', 'tests*']),
    url='https://github.com/LionelR/pyair',
    license='BSD',
    author='Lionel Roubeyrie',
    author_email='lroubeyrie@limair.asso.fr',
    description='For working with French air quality data and the Iseo XAIR database',
    long_description="""PyAir serve two purposes :
    - connect to an Iseo XAIR database for retrieving various informations like parameters and datas,
    - exploit these informations : compute statistics and compare to the French Air Reglementation.
    It's primary goal is to serve French professionnals air quality studies departments""",
    keywords="air quality xair iseo french reglementation statistics",
    install_requires=['pandas', 'cx_oracle', ],

)
