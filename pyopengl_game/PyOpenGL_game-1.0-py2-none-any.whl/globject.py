import OpenGL.GL as gl
from numpy import *
from shaderprogram import *
from ctypes import *


class VertexData:
    '''
    Class VertexData represents vertex.
    Vertex three parameters: position, normal and texture coordinates
    '''
    def __init__(self):
        '''
        Initialize vertex data
        '''
        # Initialize members
        self.pos = zeros(3, 'f')
        self.nor = zeros(3, 'f')
        self.tex = zeros(2, 'f')


class GLObject:
    '''
    GLObject represents OpenGL-drawable object.
    GLObject contains set of points and set of it's indices for all triangles of the object.
    Also GLObject have Vertex Array Object and Vertex Buffer Objects.
    '''
    def __init__(self):
        '''
        Initialize GLObject
        '''
        # Initialize members
        self.pData = None
        self.pIndices = None
        self.vao = None
        self.vbo = None

    def release(self):
        '''
        Delete Vertex Array Object and Vertex Buffer Objects
        '''
        if self.vbo:
            gl.glDeleteBuffers(2, self.vbo)
        if self.vao:
            gl.glDeleteVertexArrays(1, self.vao)
            self.vao = None

    def initGLBuffers(self):
        '''
        Initialize Vertex Array Object and Vertex Buffer Objects and fill them with data from pData and pIndices
        '''
        # Delete old VAO and VBOs
        if self.vbo:
            gl.glDeleteBuffers(2, self.vbo)
        if self.vao:
            gl.glDeleteVertexArrays(1, self.vao)
            self.vao = None

        # Create new VAO and VBOs
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        self.vbo = gl.glGenBuffers(2)

        # Convert pData into array of floats
        data = array([], 'f')
        for i in self.pData:
            data = concatenate((data, i.pos))
            data = concatenate((data, i.nor))
            data = concatenate((data, i.tex))

        # Fill first VBO with points
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, (gl.GLfloat * len(data))(*data), gl.GL_STATIC_DRAW)

        # Fill second VBO with indices
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.vbo[1])
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, (gl.GLuint * len(self.pIndices))(*self.pIndices), gl.GL_STATIC_DRAW)

        # Setup position array
        gl.glVertexAttribPointer(POSITION_LOCATION, 3, gl.GL_FLOAT, gl.GL_FALSE,
            8 * sizeof(gl.GLfloat), c_void_p(0 * sizeof(gl.GLfloat)))
        gl.glEnableVertexAttribArray(POSITION_LOCATION)

        # Setup normal array
        gl.glVertexAttribPointer(NORMAL_LOCATION, 3, gl.GL_FLOAT, gl.GL_FALSE,
            8 * sizeof(gl.GLfloat), c_void_p(3 * sizeof(gl.GLfloat)))
        gl.glEnableVertexAttribArray(NORMAL_LOCATION)

        # Setup texture array
        gl.glVertexAttribPointer(TEXTURE_LOCATION, 2, gl.GL_FLOAT, gl.GL_FALSE,
            8 * sizeof(gl.GLfloat), c_void_p(6 * sizeof(gl.GLfloat)))
        gl.glEnableVertexAttribArray(TEXTURE_LOCATION)

        # Unbind VAO
        gl.glBindVertexArray(0)

    def draw(self):
        '''
        Draw object
        '''
        # Bind VAO
        gl.glBindVertexArray(self.vao)
        # Draw
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.pIndices), gl.GL_UNSIGNED_INT, None)
        # Unbind VAO
        gl.glBindVertexArray(0)
