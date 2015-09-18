from setuptools import setup, Extension, find_packages

sha3 = Extension(
    'keccak.sha3',
    sources=['lib/sha3.c'],
    depends=['lib/compiler.h', 'lib/sha3.h'],
    extra_compile_args=["-Isrc/", "-std=gnu99", "-Wall"]
)


setup(
    name="pykeccak",
    version='0.2.0',
    description="Keccak 256 hashing for PyPy2",
    author="Jacob Stenum Czepluch",
    author_email="j.czepluch@gmail.com",
    url="https://github.com/czepluch/pykeccak",
    license="MIT",
    packages=find_packages(exclude=["_cffi_build", "_cffi_build/*"]),
    ext_modules=[sha3],
    install_requires=["cffi>=1.2.1"],
    setup_requires=["cffi>=1.2.1"],
    cffi_modules=["_cffi_build/keccak_build.py:ffi"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    zip_safe=False
)
