#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

try:
    from docfly.member import Package, Module
except ImportError:
    from .member import Package, Module

import os

class DocflyError(Exception):
    pass

class Docfly():
    """The docfly main class.

    :param package_name: the importable package name
    :type package_name: str

    :param dst: default "_source", 
    :type dst: str
    
    :param ignore: default list, 
    :type ignore: list of str
    """
    def __init__(self, package_name, dst="_source", ignore=[]):
        if "." in package_name:
            raise Exception("package_name has to be a root package.")
        
        self.package_name = package_name
        self.package = Package(package_name)
        self.dst = dst
        self.ignore = [i.replace(".py", "") for i in ignore]
        
    def fly(self):
        """Generate doc tree.
        """
        dst = self.dst # create an temp alias
        
        try:
            os.mkdir(dst)
        except:
            pass
        
        # delete everything already exists
        for path in os.listdir(os.path.abspath(dst)):
            try:
                os.remove(os.path.join(dst, self.package_name))
            except:
                pass
            
        # create .rst files                
        for package, fullname, packages, modules in self.package.walk():

            if not self.isignored(package):
                dir_path = os.path.join( *(
                        [dst, ] + fullname.split(".")
                        ) )
                init_path = os.path.join(dir_path, "__init__.rst")
                
                self.make_dir(dir_path)
                
                self.make_file(init_path, self.generate_package_content(package))
                
                for module in modules:

                    if not self.isignored(module):
                        module_path = os.path.join(dir_path, module.name + ".rst")
                        self.make_file(module_path, self.generate_module_content(module))
        
    def isignored(self, mod_or_pkg):
        """Find whether if we need include a :class:`docfly.member.Package` or
        :class:`docfly.member.Module`.
        
        **中文文档**
        
        根据全名判断一个包或者模块是否需要被ignore.
        """
        for pattern in self.ignore:
            if pattern == mod_or_pkg.fullname:
                return True
        return False
    
    def make_dir(self, abspath):
        """Make an empty directory.
        """
        try:
            os.mkdir(abspath)
            print("made %s" % abspath)
        except:
            pass
    
    def make_file(self, abspath, text):
        """Make a file with utf-8 text.
        """
        try:
            with open(abspath, "wb") as f:
                f.write(text.encode("utf-8"))
            print("made %s" % abspath)
        except:
            pass
        
    def generate_package_content(self, package):
        """Generate package.rst text content.
        """
        if isinstance(package, Package):
            header = "%s\n%s" % (package.name, "=" * len(package.name))
            automodule = "\n\n.. automodule:: %s\n\t:members:" % package.fullname
            header2 = "\n\nsubpackage and modules\n----------------------"
            toctree = "\n\n.. toctree::\n   :maxdepth: 1\n\n"
            
            lines = list()
            for p in package.subpackage.values():
                if not self.isignored(p):
                    lines.append("\t%s <%s>" % (p.name, p.name + "/__init__"))
            for m in package.module.values():
                if not self.isignored(m):
                    lines.append("\t%s <%s>" % (m.name, m.name))
                
            content = "{0}{1}{2}{3}{4}".format(
                header, 
                automodule, 
                header2, 
                toctree, 
                "\n".join(lines))

            return content
        else:
            raise Exception("%s is not a Package object" % repr(package))
    
    def generate_module_content(self, module):
        """Generate module.rst text content.
        """
        if isinstance(module, Module):
            header = "%s\n%s" % (module.name, "=" * len(module.name))
            automodule = "\n\n.. automodule:: %s\n\t:members:" % module.fullname
            content = "{0}{1}".format(header, automodule)
            return content
        else:
            raise Exception("%s is not a Module object" % repr(module))
    
if __name__ == "__main__":
    docfly = Docfly("toppackage", dst="_source", 
        ignore=["toppackage.subpackage1", 
                "toppackage.module2.py", 
                "toppackage.subpackage2.module22.py"])
    docfly.fly()
    