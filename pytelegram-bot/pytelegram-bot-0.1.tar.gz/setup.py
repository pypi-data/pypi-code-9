try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='pytelegram-bot',
    version='0.1',
    requires=['requests'],
    url='http://www.github.com/jsevilleja/pytelegram-bot',
    include_package_data=True,
    license='MIT',
    author='Joel Sevilleja',
    author_email='joel@jsevilleja.org',
    description='A module to simplify working with Telegram Bot API',
    packages = ["telegram"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
