from setuptools import setup,find_packages

setup(
        name='jiemoutils',
        version='0.7',
        description='jiemo utils',
        author='it_account@jiemodai.com',
        author_email='it_account@jiemodai.com',
        url='http://jiemo.co',
        packages=find_packages(),
        install_requires=['django', 'mako'],
)
