from setuptools import setup

setup(
    name='japan_holiday',
    version="0.0.1",
    description='Holiday in Japan from Google Calendar.',
    long_description='japan_holiday' + '\n\n' + '',
    author='haminiku',
    author_email='haminiku1129@gmail.com',
    url='https://github.com/subc/japan_holiday',
    package_dir={'japan_holiday': 'japan_holiday'},
    include_package_data=True,
    license='MIT License',
    zip_safe=False,
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
