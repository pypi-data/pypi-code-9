from setuptools import setup
import sudoku_json2pdf

setup(
    name='SudokuJson2Pdf',
    version=sudoku_json2pdf.__version__,
    author='Yassu',
    packages=['sudoku_json2pdf'],
    description=(

        'This project provides a tool which convert json file of sudoku'
        'information to pdf.'),
    long_description=open("readme.rst").read(),
    url='https://github.com/yassu/SudokuJson2Pdf',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: Freeware',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author_email='mathyassu@gmail.com',
    install_requires=[
        'reportlab',
    ],
    license=(
        'Released Under the Apache license\n'
        'https://github.com/yassu/SudokuJson2Pdf\n'
    ),
    scripts=['sudoku_json2pdf/sudoku2pdf.py'],
)
