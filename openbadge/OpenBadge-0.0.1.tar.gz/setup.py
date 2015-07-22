
from setuptools import setup, find_packages

setup(
    name='OpenBadge',
    version='0.0.1',
    url='https://github.com/thisbejim/openbadge',
    description='An Open Badges helper library',
    author='James Childs-Maidment',
    author_email='jchildsmaidment@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
    ],
    keywords='Open Badges',
    packages=find_packages(exclude=['test']),
    install_requires=['PyJWT', 'cryptography', 'hashlib']
)
