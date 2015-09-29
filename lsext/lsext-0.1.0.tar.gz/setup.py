from setuptools import setup


setup(
    name='lsext',
    version='0.1.0',
    py_modules=['lsext', 'fswalk'],

    entry_points={
        'console_scripts' : ['lsext=lsext:start_main']
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    author='Gu Zhengxiong',
    author_email='rectigu@gmail.com',
    description='File Extension Distribution Analysis',
    keywords='List Extensions, Traverse Directories',
    license='GPL',
    url='https://github.com/NoviceLive/lsext'
)
