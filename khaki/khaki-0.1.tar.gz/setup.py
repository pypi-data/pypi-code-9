from setuptools import setup, find_packages

VERSION = '0.1'

setup(
    name='khaki',
    version=VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'khaki = khaki.__main__:run',
        ],
    },
    install_requires=[
        'pyglet==1.2.3',
    ],
    include_package_data=True,

    url='https://gitlab.com/tarcisioe/khaki',
    download_url='https://gitlab.com/tarcisioe/khaki/repository/archive.tar.gz',
    keywords=['timer', 'productivity'],
    maintainer='Tarcísio Eduardo Moreira Crocomo',
    maintainer_email='tarcisio.crocomo+pypi@gmail.com',
    description='A simple Pomodoro timer using curses (and pyglet for audio playback)',
)
