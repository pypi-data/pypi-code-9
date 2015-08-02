from distutils.core import setup
 
setup(
    name = 'arc_library',
    version = '1.0.41',
    # py_modules = ['arc_django_models', 'arc_functions', 'arc_jsonobject', 'arc_storage', 'arc_tag'],
	#py_modules = ['arc_library'],
    packages = ['arclib', 'arclib/django', 'arclib/gae', 'arclib/http'],
    author = 'Arcanelux',
    author_email = 'Arcanelux@gmail.com',
    url = 'iiii.so',
    description = 'If imageinfo function\'s instance path file is not exist, return empty dict and \'has_file\' keyword value is False',
)


