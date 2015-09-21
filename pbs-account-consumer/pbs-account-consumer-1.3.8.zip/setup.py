from setuptools import setup, find_packages
try:
    import six
    py2 = six.PY2
except ImportError:
    py2 = False


setup(
    name='pbs-account-consumer',
    version='1.3.8',
    description='PBS Account Consumer',
    author='PBS Core Services Team',
    author_email='PBSi-Team-Core-Services@pbs.org',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # Django can't find templates inside zips
    install_requires=(
        'Django>=1.4',
        'python-openid>=2.2.5' if py2 else 'python3-openid>=3.0.6',
    )
)
