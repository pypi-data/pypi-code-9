import imp


def package_location(name):

    f, filename, description = imp.find_module(name)
    return filename

def package_load(name):
    f, filename, description = imp.find_module(name)
    print "Loading:", name, filename
    print "FFF", f
    print "DDD", description
    dynamic_package = imp.load_module(name, f, filename, description)
    return dynamic_package

print package_location('cmd3')

cmd3 = package_load('cmd3')

print cmd3
