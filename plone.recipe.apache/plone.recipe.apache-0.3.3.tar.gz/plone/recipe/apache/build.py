import os

import logging, tempfile, setuptools
import urlparse, shutil, urllib2

from zc.recipe.cmmi import Recipe as CMMIRecipe

class BuildRecipe(CMMIRecipe):

    def __init__(self, buildout, name, options):
        #super(BuildRecipe, self).__init__(buildout, name, options)
        CMMIRecipe.__init__(self, buildout, name, options)
        self.name=name
        self.options=options
        self.buildout=buildout
        self.logger=logging.getLogger(self.name)

        self.svn=options.get("svn", None)
        self.url=options.get("url", None)
        if not (self.svn or self.url):
            self.logger.error(
                    "You need to specify either a URL or subversion repository")
            raise zc.buildout.UserError("No download location given")

        # If we use a download, then look for a shared Apache installation directory
        if self.svn is None and buildout['buildout'].get('apache-directory') is not None:
            print 'download already there'
            _, _, urlpath, _, _, _ = urlparse.urlparse(self.url)
            fname = urlpath.split('/')[-1]
            # cleanup the name a bit
            for s in ('.tar', '.bz2', '.gz', '.tgz'):
                fname = fname.replace(s, '')
            location = options['location'] = os.path.join(
                buildout['buildout']['apache-directory'],fname)
            options['shared-apache'] = 'true'
        else:
            # put it into parts
            location = options['location'] = os.path.join(
                buildout['buildout']['parts-directory'],self.name)

        options["source-location"]=os.path.join(location, "source")
        options["binary-location"]=os.path.join(location, "install")
        #options["daemon"]=os.path.join(location, "apache")

        # Set some default options
        buildout['buildout'].setdefault('download-directory',
                os.path.join(buildout['buildout']['directory'], 'downloads'))

    def install(self):
        installed = self.installApache()
        self.addScriptWrappers()
        return installed
        #if self.url and self.options.get('shared-apache') == 'true':
        #    # If the apache installation is shared, only return non-shared paths
        #    return self.options.created()
        #return self.options.created(self.options["location"])

    def installApache(self):
        location=self.options["location"]
        if os.path.exists(location):
            # If the apache installation exists and is shared, then we are done
            if self.options.get('shared-apache') == 'true':
                return
            else:
                shutil.rmtree(location)
        os.mkdir(location)
        self.downloadApache()
        return self.compileApache()
        
    def addScriptWrappers(self):
        bintarget=self.buildout["buildout"]["bin-directory"]

        for dir in ["sbin", "bin"]:
            dir=os.path.join(self.options["location"], dir)
            if not os.path.isdir(dir):
                continue
            if 'apachectl' in os.listdir(dir):
                file = 'apachectl'
                self.logger.info("Adding script wrapper for %s" % file)
                target=os.path.join(bintarget, file)
                f=open(target, "wt")
                print >>f, "#!/bin/sh"
                print >>f, 'exec %s "$@"' % os.path.join(dir, file)
                f.close()
                os.chmod(target, 0755)
                #self.options.created(target)

    def downloadApache(self):
        download_dir=self.buildout['buildout']['download-directory']

        if self.svn:
            self.logger.info("Checking out apache from subversion.")
            assert os.system("svn co %s %s" % (self.options["svn"], self.options["source-location"]))==0
        else:
            self.logger.info("Downloading apache tarball.")
            if not os.path.isdir(download_dir):
                os.mkdir(download_dir)

            _, _, urlpath, _, _, _ = urlparse.urlparse(self.url)
            tmp=tempfile.mkdtemp("buildout-"+self.name)

            try:
                fname=os.path.join(download_dir, urlpath.split("/")[-1])
                if not os.path.exists(fname):
                    f=open(fname, "wb")
                    try:
                        f.write(urllib2.urlopen(self.url).read())
                    except:
                        os.remove(fname)
                        raise
                    f.close()

                setuptools.archive_util.unpack_archive(fname, tmp)

                files=os.listdir(tmp)
                shutil.move(os.path.join(tmp, files[0]), self.options["source-location"])
            finally:
                shutil.rmtree(tmp)

    def compileApache(self):
        os.chdir(self.options["source-location"])
        self.logger.info("Compiling Apache")
        
        extra = """ --with-prefix=%s \
                    --with-included-apr \
                    --enable-headers \
                    --enable-rewrite \
                    --enable-proxy \
                """ % self.options["binary-location"]
                
        modules = self.options.get('modules', '').split(os.linesep)
        for mod in modules:
            mod = mod.strip()
            if mod:
                extra += '--enable-%s ' % mod
                
        # This sets the options dict AFTER the superclass has already
        # parsed it to self.extra_options, thus no configure settings.
        #self.options['extra_options'] = extra
        # Instead, set the super's class var.
        # Newly documented feature: append to any existing recipe
        # 'extra_options' settings parsed by the superclass so we can
        # provide things like "--with-mpm=worker --with-port=8888".
        self.extra_options = self.extra_options + ' ' + extra
        self.logger.info("Configuring with options: %s" % self.extra_options)

        # uses cmmi installer
        installed = CMMIRecipe.install(self)
        #installed = '.../plone.recipe.apache/plone/recipe/apache/tests/apache'
        return installed

    def update(self):
        """updater"""
        pass
