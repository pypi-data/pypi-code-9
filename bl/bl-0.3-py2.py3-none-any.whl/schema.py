
import os, re, sys, subprocess, tempfile
from bl.text import Text

class Schema(Text):

    def __init__(self, fn):
        """relaxng schema initialization.
        fn = the schema filename (required)
        """
        Text.__init__(self, fn=fn)

    def trang(self, ext='.rng'):
        """use trang to create a schema with the given format extension
        SIDE EFFECT: creates a new file on the filesystem."""
        trangfn = os.path.join(os.path.dirname(__file__), 'lib', 'trang.jar')
        outfn = os.path.splitext(self.fn)[0] + ext
        stderr = tempfile.NamedTemporaryFile()
        try:
            result = subprocess.check_call(
                ["java", "-jar", trangfn, self.fn, outfn],
                universal_newlines=True,
                stderr=stderr)
        except subprocess.CalledProcessError as e:
            f = open(stderr.name, 'r+b')
            output = f.read(); f.close()
            raise RuntimeError(str(output, 'utf-8')).with_traceback(sys.exc_info()[2]) from None
        if result==0:
            return outfn
    
    @classmethod
    def from_tag(cls, tag, schema_path, ext='.rnc'):
        """load a schema using an element's tag"""
        return cls(fn=cls.filename(tag, schema_path, ext=ext))

    @classmethod
    def filename(cls, tag, schema_path, ext='.rnc'):
        return os.path.join(schema_path, cls.dirname(tag), cls.basename(tag, ext=ext))

    @classmethod
    def dirname(cls, namespace):
        """convert a namespace url to a directory name. 
            Also accepts an Element 'tag' with namespace prepended in {braces}."""
        md = re.match("^\{?(?:[^:]+:/{0,2})?([^\}]+)\}?", namespace)
        if md is not None:
            dirname = md.group(1).replace("/", "_").replace(":", "_")
        else:
            dirname = ''
        return dirname

    @classmethod
    def basename(cls, tag, ext='.rnc'):
        return re.sub("\{[^\}]*\}", "", tag) + ext
