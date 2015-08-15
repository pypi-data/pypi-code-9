import OpenGL.GL as gl


class Shader:
    '''
    Class Shader represents OpenGL shader
    '''
    def __init__(self):
        '''
        Initialize shader
        '''
        # Initialize memvers
        self.shaderType = None
        self.shaderObject = None

    def getShaderType(self):
        '''
        Get shader type
        @return: shader type
        '''
        return self.shaderType

    def getShaderObject(self):
        '''
        Get shader object
        @return: shader object
        '''
        return self.shaderObject

    def read(self, filename, type):
        '''
        Read shader source from file
        @param filename: name of file
        @param type: shader type
        '''
        self.shaderType = type
        self.shaderObject = gl.glCreateShader(self.shaderType)
        file = open(filename, "r").read()
        gl.glShaderSource(self.shaderObject, file)

    def compile(self):
        '''
        Compile shader
        '''
        gl.glCompileShader(self.shaderObject)

    def readAndCompile(self, filename, type):
        '''
        Read shader source from file and compile
        @param filename: name of file
        @param type: shader type
        '''
        self.read(filename, type)
        self.compile()

    def release(self):
        '''
        Free shader object
        '''
        if self.shaderObject:
            gl.glDeleteShader(self.shaderObject)
            self.shaderObject = None