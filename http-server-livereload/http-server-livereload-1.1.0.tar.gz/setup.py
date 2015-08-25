from setuptools import setup

setup(
    name='http-server-livereload',
    version='1.1.0',
    description='A monkey patch of http.server to call livereload when '
    'server_forever is called. This is compatible with flask reload '
    'and tiny-lr (grunt watch).',
    author="Mounier Florian",
    author_email="mounier.florian@gmail.com",
    license='MIT',
    platforms="Any",
    packages=['http_server_livereload'],
    keywords=[
        'flask', 'livereload', 'grunt', 'watch', 'tiny-lr'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
