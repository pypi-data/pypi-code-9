import platform
if platform.python_version().startswith('2'):
    import xmlrpclib
else:
    import xmlrpc.client as xmlrpclib
import pkg_resources


def update():
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    available = pypi.package_releases('iodine')[0]
    installed = pkg_resources.get_distribution('iodine').version
    if installed < available:
        print(
            "New version of iodine is available: pip install --upgrade iodine")
