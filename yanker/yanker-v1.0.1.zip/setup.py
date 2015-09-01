from distutils.core import setup

setup(
    name='yanker',
    version='v1.0.1',
    packages=['yanker'],
    url='http://github.com/battleroid/yanker.git',
    download_url='',
    license='MIT License',
    keywords='yanker youtube youtube-dl download videos',
    author='Casey Weed',
    author_email='me@caseyweed.net',
    description='Basic multithreaded console frontend for youtube-dl.',
    install_requires=[
        'pyperclip>=1.5.11',
        'youtube-dl>=2015.8.28',
        'docopt>=0.6.2'
    ],
    setup_requires=[],
    entry_points={
        'console_scripts': ['yanker = yanker.yanker:run']
    },
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet'
    ]
)
