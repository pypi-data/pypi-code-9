#from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(
    name='mfe_fwaas',
    version='0.5',
    packages=find_packages(),
    scripts=['mfe_fwaas/mfe-neutron-db-manage'],
    package_data = {
        '' : ['mfe-neutron-db-manage', "alembic.ini"]
    },
    zip_safe=False
)
