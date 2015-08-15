import setuptools

setuptools.setup(
    name = "PyOpenGL_game",
    version = "1.01",
    author = "Vladimir Zhukov",
    author_email = "zhvv117@gmail.com",
    description = "Simple OpenGL game",
    license = "MIT",
    packages=["PyOpenGL_game"],
    package_data={
        "PyOpenGL_game": ["data/*", "localization/*.po*",
            "localization/ru/LC_MESSAGES/*", "*.vert", "*.frag", "event.list",
            "libglfw.so"],
    },
    include_package_data=True,
    zip_safe=False,
    long_description= "Simple OpenGL game",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points = {
        "console_scripts": [
            "pyopenglgame = PyOpenGL_game.main:main",
        ]
    },
    install_requires = ["numpy", "pyopengl", "pypng", "pillow"]
)
