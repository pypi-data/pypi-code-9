from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()
setup(
    name="kubetemplate",

    version="0.0.1",

    author="Akshaya Acharya",
    author_email="akshaya@hasura.io",

    packages=["kubetemplate"],

    include_package_data=True,

    url="https://github.com/hasura/kubetemplate",

    license="MIT",

    keywords="kubernetes template templating jinja pangaea",
    description="Kubernetes specific helpers and Jinja templating",
    long_description=readme(),

    install_requires=[
        "jinja2",
        "argh"
    ],

    entry_points = {
        'console_scripts': ['kubet=kubetemplate.command:main']
    }
)
