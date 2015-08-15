from globject import *


class objectQuad(GLObject):
    '''
    Class objectQuad represents drawable quad
    '''
    def __init__(self):
        '''
        Initialize quad object
        '''
        GLObject.__init__(self)
        self.pData = []
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([cond1 - 0.5, cond2 - 0.5, 0], 'f')
            vd.nor = array([0, 0, 1], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        self.pIndices = array([0, 1, 3, 2, 0, 3], 'i')
        self.initGLBuffers()
