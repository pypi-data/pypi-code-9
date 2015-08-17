import logging, os, zc.buildout, sys, shutil

class ZipEggs:
    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        if options['target'] is None:
            raise zc.buildout.UserError('Invalid Target')
        if options['source'] is None:
            raise zc.buildout.UserError('Invalid Source')


    def zipit(self):
        target = self.options['target']
        if not os.path.exists(target):
            os.mkdir(target)
        path = self.options['source']
        for dirs in os.listdir(path):
            try:
                source = os.path.join(path, dirs)
                dist = "%s/%s" % (target, dirs)
                print "%s > %s" % (source, dist)
                shutil.make_archive(dist, "zip", source)
                os.rename(dist+".zip", dist)
            except OSError:
                print "ignore %s" % dirs
        return []

    def install(self):
        return self.zipit()

    def update(self):
        return self.zipit()
