import os
import socket
import itertools
import re
from lxml.etree import tostring, fromstring, XML
from lxml.builder import E

class stanford():
    def __init__( self, jarpath, debug=False ):
        import jpype
        assert os.path.isfile(jarpath) , "JAR file not found: " + jarpath
        jarpath = os.path.abspath(jarpath)
        classpath = ":".join([
            os.path.dirname(os.path.realpath(__file__)),
            os.path.dirname(jarpath),
            jarpath
        ])
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path="+classpath )
        self.segmenter = jpype.JClass("DemoSeg")
        self.segmenter.debug = debug
    def segment( self, sent ):
        res = self.segmenter.segment(sent)
        return [ res.get(i) for i in range( res.size() ) ]
    def close(self):
        jpype.shutdownJVM()

class Ckip():


    CKIP_SERVER_IP, CKIP_SERVER_PORT = "140.109.19.104", 1501

    def __init__( self, username, password, server_ip = CKIP_SERVER_IP, server_port = CKIP_SERVER_PORT ):
        self.username = username
        self.password = password

        self._server_ip = server_ip
        self._server_port = server_port

    def segment( self, sent ):
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect( (self._server_ip, self._server_port) )

        encoding = "big5"
        tree = E.wordsegmentation(
            E.option(showcategory='1'),
            E.authentication(username=self.username,password=self.password),
            E.text(sent),
        version='0.1')
        xmlstring = tostring(tree, encoding=encoding, xml_declaration=True)


        sock.send( xmlstring )
        data = sock.recv( 10240 )
        sock.close()
        return self.parse_result( data.decode(encoding) )

    def parse_result( self, string ):
        root = XML(string)
        sents = root.xpath(".//sentence")
        return list(
            itertools.chain.from_iterable( re.findall("\u3000(\w+)\(\w+\)""",sent.text) for sent in sents )
        )


