try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

pkgdir = {'': 'python%s' % sys.version_info[0]}
VERSION = '2.1.0'

setup(
    name='tencentyun',
    version=VERSION,
    author='Jay Li, Jamis Hoo',
    author_email='jayli@tencent.com, hoojamis@gmail.com',
    url='https://github.com/tencentyun/python-sdk',
    download_url='https://codeload.github.com/tencentyun/python-sdk/tar.gz/%s' % VERSION,
    description='Pyton 2/3 SDK for app.qcloud.com',
    license='MIT',
    # long_description="",
    package_dir=pkgdir,
    packages=['tencentyun'],
    classifiers=[ ],
)

