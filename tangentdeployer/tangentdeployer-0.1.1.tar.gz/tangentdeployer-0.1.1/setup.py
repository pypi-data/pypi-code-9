from setuptools import setup, find_packages

setup(
    name='tangentdeployer',
    packages=find_packages(''),
    version='0.1.1',
    description='A Fabric deploy script for AWS based projects',
    author='Chris McKinnel',
    author_email='chris.mckinnel@tangentsnowball.com',
    url='https://github.com/tangentlabs/tangent-deployer',
    download_url='https://github.com/tangentlabs/tangent-deployer/tarball/0.1',
    keywords=['deployment', 'fabric', 'tangent'],
    classifiers=[],
    install_requires=['jinja2==2.7.3']
)
