from setuptools import setup, find_packages

setup(
    name="parchment",
    version="0.1.0",
    packages=find_packages(),
    description="a simple static site generator",
    include_package_data=True,
    author="Taff Gao",
    author_email="gaotongfei1995@gmail.com",
    url="https://github.com/gaotongfei/parchment",
    install_requires=[
        "click",
        "Cython",
        "Jinja2",
        "MarkupSafe",
        "mistune",
        "PyYAML",
        "wheel"
    ],
    entry_points='''
        [console_scripts]
        parchment_init = src.commands.init_command:init
        parchment_g = src.commands.generate_command:generate
        parchment_generate = src.commands.generate_command:generate
    ''',
)
