from setuptools import setup, find_packages


setup(
    name='frasco-invoicing',
    version='0.2',
    url='http://github.com/frascoweb/frasco-invoicing',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description="Invoicing for Frasco",
    packages=find_packages(),
    package_data={
        'frasco_invoicing': [
            'emails/*.html']
    },
    zip_safe=False,
    platforms='any',
    install_requires=[
        'frasco',
        'frasco-models>=0.4'
    ]
)
