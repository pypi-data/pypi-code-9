from setuptools import setup, find_packages

setup(
    
    name = 'djangocms-rosetta',
    
    version = '0.0',
    
    description = 'Link to the rosetta interface in the Django CMS Toolbar',
    
    url = 'https://github.com/philippze/djangocms-rosetta',
    
    author = 'Philipp Zedler',
    author_email = 'philipp@neue-musik.com',
    
    license = 'MIT',
    
    keywords = 'Django translation rosetta',
    
    packages = find_packages(),
    
    install_requires=['Django>=1.7', 'django-cms>=3.1', 'django-rosetta>=0.7']
    
)
