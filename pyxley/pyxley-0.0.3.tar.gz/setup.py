from distutils.core import setup

setup(
    name='pyxley',
    version='0.0.3',
    author='Nicholas Kridler',
    author_email='nmkridler@gmail.com',
    license='MIT',
    description='Python tools for building Flask-based web applications',
    packages = ['pyxley', 'pyxley.filters', 'pyxley.charts', 'pyxley.charts.mg',
        'pyxley.charts.datatables', 'pyxley.charts.datamaps'],
    long_description='Python tools for building Flask-based web applications using React.js',
    url='https://github.com/stitchfix/pyxley',
    keywords=['pyreact', 'flask'],
    classifiers=[
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'pyreact',
        'flask',
        'pandas'
    ]
)
