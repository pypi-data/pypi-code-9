from globject import *


class objectCube(GLObject):
    '''
    Class objectCube represents drawable cube
    '''
    def __init__(self):
        '''
        Initialize cube object
        '''
        GLObject.__init__(self)
        self.pData = []
        self.pIndices = []
        # Front
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([cond1 - 0.5, cond2 - 0.5, -0.5], 'f')
            vd.nor = array([0, 0, -1], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        s = 0
        self.pIndices += [0 + s, 3 + s, 1 + s, 2 + s, 3 + s, 0 + s]
        # Back
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([cond1 - 0.5, cond2 - 0.5, 0.5], 'f')
            vd.nor = array([0, 0, 1], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        s = 4
        self.pIndices += [3 + s, 0 + s, 1 + s, 2 + s, 0 + s, 3 + s]
        # Left
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([-0.5, cond1 - 0.5, cond2 - 0.5], 'f')
            vd.nor = array([-1, 0, 0], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        s = 8
        self.pIndices += [0 + s, 3 + s, 1 + s, 2 + s, 3 + s, 0 + s]
        # Right
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([0.5, cond1 - 0.5, cond2 - 0.5], 'f')
            vd.nor = array([1, 0, 0], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        s = 12
        self.pIndices += [3 + s, 0 + s, 1 + s, 2 + s, 0 + s, 3 + s]
        # Top
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([cond1 - 0.5, 0.5, cond2 - 0.5], 'f')
            vd.nor = array([0, 1, 0], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        s = 16
        self.pIndices += [0 + s, 3 + s, 1 + s, 2 + s, 3 + s, 0 + s]
        # Down
        for i in range(4):
            vd = VertexData()
            cond1 = 0
            cond2 = 0
            if i % 2:
                cond1 = 1
            if i > 1:
                cond2 = 1
            vd.pos = array([cond1 - 0.5, -0.5, cond2 - 0.5], 'f')
            vd.nor = array([0, -1, 0], 'f')
            vd.tex = array([cond1, 1 - cond2], 'f')
            self.pData.append(vd)
        s = 20
        self.pIndices += [3 + s, 0 + s, 1 + s, 2 + s, 0 + s, 3 + s]
        self.pIndices = array(self.pIndices, 'i')
        self.initGLBuffers()
