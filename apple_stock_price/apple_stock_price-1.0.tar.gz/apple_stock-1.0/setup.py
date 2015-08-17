from distutils.core import setup

### now we just need to set the metadata for the file
# the content will be inside a tuple 
setup(
	name = 'apple_stock', 
	version = '1.0', 
	description = 'a simple apple stock scraper', 
	author = 'Tasdik Rahman', 
	py_module = ['apple_stock_price']
)