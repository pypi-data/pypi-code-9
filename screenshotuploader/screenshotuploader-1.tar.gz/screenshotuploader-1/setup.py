
from setuptools import setup

setup(name="screenshotuploader",
	version="1",
	description="Automagically captures the screenshot of the screen , uploads in imgurl , copies the url into clipboard , deletes the created image file from your desktop",
	url="https://github.com/yask123/AutoScreenshotUploader",
	author="Yask Srivastava",
	author_email="yask123@gmail.com",
	license='MIT',
	packages=["screenshotuploader"],
	scripts=["bin/screenshotuploader"],
	zip_safe=False)
