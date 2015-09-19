from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from subprocess import call


class PasteurizeBuildCommand(build_py):
    def run(self):
        call(["pip", "install", "future"])
        call(["pasteurize", "./src/sqlalchemy_fp"])
        build_py.run(self)

description = "A wrapper around SQLAlchemy for more functional ORM programming"

setup(
    name="sqlalchemy-fp",
    version="0.1",
    description=description,
    url="http://github.com/jackfirth/sqlalchemy-fp",
    author="Jack Firth",
    author_email="jackhfirth@gmail.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    setup_requires=["future"],
    install_requires=[
        "psycopg2",
        "sqlalchemy",
        "pyramda",
        "attrdict"
    ],
    tests_require=["nose", "coverage"],
    cmdclass={
        "build_py": PasteurizeBuildCommand
    },
    zip_safe=False
)
