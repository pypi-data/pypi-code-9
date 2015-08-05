from setuptools import setup, find_packages


setup(
    name='frasco-admin',
    version='0.2.1',
    url='http://github.com/frascoweb/frasco-admin',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description="Admin interface for Frasco",
    packages=find_packages(),
    package_data={
        'frasco_admin': [
            'blueprint/static/*.css',
            'blueprint/static/*.js',
            'blueprint/templates/admin/*.html',
            'macros.html']
    },
    zip_safe=False,
    platforms='any',
    install_requires=[
        'frasco',
        'frasco-bootstrap',
        'inflection'
    ]
)
