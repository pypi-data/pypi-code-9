import OpenGL.GL as gl
from shader import Shader

POSITION_LOCATION = 0
NORMAL_LOCATION = 1
TEXTURE_LOCATION = 2

TEXTURE_SAMPLER_LOCATION = 29
TEXTURE_FLAG_LOCATION = 30

MODEL_MATRIX_LOCATION = 13
VIEW_MATRIX_LOCATION = 17
NORMAL_MATRIX_LOCATION = 21
PROJECTION_MATRIX_LOCATION = 25

COLOR_LOCATION = 31
LIGHTING_FLAG_LOCATION = 32


class ShaderProgram:
    '''
    Class ShaderProgram represents OpenGL shader program
    '''
    def __init__(self):
        '''
        Initialize shader program
        '''
        # Initialize members
        self.vertexShader = None
        self.fragmentShader = None
        self.programObject = None

    def init(self, vertexShaderName, fragmentShaderName):
        '''
        Initialize shader program
        @param vertexShaderName: vertex shader filename
        @param fragmentShaderName: fragment shader filename
        @return:
        '''
        # Initialize vertex shader
        self.vertexShader = Shader()
        self.vertexShader.readAndCompile(vertexShaderName, gl.GL_VERTEX_SHADER)
        self.fragmentShader = Shader()
        # Initialize fragment shader
        self.fragmentShader.readAndCompile(fragmentShaderName, gl.GL_FRAGMENT_SHADER)
        # Create shader program
        self.programObject = gl.glCreateProgram()
        gl.glAttachShader(self.programObject, self.vertexShader.getShaderObject())
        gl.glAttachShader(self.programObject, self.fragmentShader.getShaderObject())
        gl.glBindFragDataLocation(self.programObject, gl.GL_NONE, "fragColor")
        gl.glLinkProgram(self.programObject)

    def getProgramObject(self):
        '''
        Get program object
        @return: program object
        '''
        return self.programObject
