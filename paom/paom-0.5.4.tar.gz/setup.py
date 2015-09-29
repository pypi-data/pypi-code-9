from setuptools import find_packages, setup
setup(
    name='paom',
    include_package_data=True,
    package_data={
        'resources': [
            '__init__.py',
            'orders.py',
            'products.py',
            'users.py',
            'quizzes.py'
        ]
    },
    packages=find_packages(exclude=["dist"]),
    version='0.5.4',
    license='MIT',
    description='API integration of PAOM',
    author='Meredith Finkelstein Chang',
    author_email='meredith@printallover.me',
    url='https://bitbucket.org/msrobot0/paom_python_api', # use the URL to the github repo
    download_url='https://bitbucket.org/msrobot0/paom_python_api/tarball/0.3',
    keywords=['paom', 'python', 'paom api'], # arbitrary keywords
    classifiers=[],
    install_requires=["requests"],
)
