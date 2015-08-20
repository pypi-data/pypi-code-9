from setuptools import find_packages, setup
setup(
    name='paom',
    include_package_data=True,
    package_data={
        'resources': [
            '__init__.py',
            'cart_items.py',
            'carts.py',
            'categories.py',
            'collections.py',
            'designs.py',
            'orders.py',
            'products.py',
            'users.py'
        ]
    },
    packages=find_packages(exclude=["dist"]),
    version='0.5.1',
    license='MIT',
    description='A random test lib',
    author='Meredith Finkelstein Chang',
    author_email='meredith@printallover.me',
    url='https://bitbucket.org/msrobot0/paom_python_api', # use the URL to the github repo
    download_url='https://bitbucket.org/msrobot0/paom_python_api/tarball/0.3', # I'll explain this in a second
    keywords=['paom', 'python', 'paom api'], # arbitrary keywords
    classifiers=[],
    install_requires=["requests"],
)
