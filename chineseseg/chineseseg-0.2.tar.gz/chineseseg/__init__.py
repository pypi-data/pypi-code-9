import jpype
import os

class stanford():
    def __init__( self, jarpath ):
        assert os.path.isfile(jarpath) , "JAR file not found: " + jarpath
        jarpath = os.path.abspath(jarpath)
        classpath = ":".join([
            os.path.dirname(os.path.realpath(__file__)),
            os.path.dirname(jarpath),
            jarpath
        ])
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path="+classpath )
        self.segmenter = jpype.JClass("DemoSeg")
    def segment( self, sent ):
        res = self.segmenter.segment(sent)
        return [ res.get(i) for i in range( res.size() ) ]
    def close(self):
        jpype.shutdownJVM()


