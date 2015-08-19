from shaderprogram import *
import OpenGL.GL as gl
from glutils import *
from texture import Texture
import glfont

TEXT_COUNT = 64


class GUI:
    '''
    Class GUI provide methods to interact with OpenGL
    '''
    window_height = 480
    window_width = 640
    aspect = float(window_width) / window_height

    shaderProgram = ShaderProgram()

    eye = zeros(3, 'f')
    cen = zeros(3, 'f')
    up  = array([0, 1, 0], 'f')

    viewMatrix = identity(4, 'f')
    modelMatrix = identity(4, 'f')
    projectionMatrix = identity(4, 'f')
    normalMatrix = identity(4, 'f')

    textures = []

    def __init__(self):
        '''
        Initialize GUI
        '''
        self.__initOpenGL()

    def __initOpenGL(self):
        '''
        Initialize OpenGL
        '''
        # Setup depth test
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glClearDepth(1.0)

        # Setup cull face
        gl.glEnable(gl.GL_CULL_FACE)

        # Setup alpha blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Create shader program
        self.shaderProgram.init("Vertex.vert", "Fragment.frag")
        gl.glUseProgram(self.shaderProgram.getProgramObject())

        # Create texture objects
        gl.glActiveTexture(gl.GL_TEXTURE0)
        tex_ids = gl.glGenTextures(TEXT_COUNT)
        for i in range(TEXT_COUNT):
            self.textures.append(Texture(tex_ids[i]))

        # Initialize some shader uniforms
        gl.glUniform1i(TEXTURE_SAMPLER_LOCATION, 0)
        gl.glUniform1i(TEXTURE_FLAG_LOCATION, 0)
        gl.glUniform1i(LIGHTING_FLAG_LOCATION, 0)

    def __recalcAspect(self):
        '''
        Recalculate screen aspect ratio
        '''
        if self.window_height:
            self.aspect = float(self.window_width) / self.window_height

    def getWindowHeight(self):
        '''
        Get window height
        @return: window height
        '''
        return self.window_height

    def setWindowHeight(self, h):
        '''
        Set window height
        @param h:  window height
        '''
        self.window_height = h
        self.__recalcAspect()

    def getWindowWidth(self):
        '''
        Get window width
        @return: window width
        '''
        return self.window_width

    def setWindowWidth(self, w):
        '''
        Set window width
        @param w: window width
        '''
        self.window_width = w
        self.__recalcAspect()

    def sendMatrices(self):
        '''
        Send projection, view and model matrices to vertex shader
        '''
        self.normalMatrix = transpose(linalg.inv(mul(self.viewMatrix, self.modelMatrix)))
        gl.glUniformMatrix4fv(MODEL_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.modelMatrix))
        gl.glUniformMatrix4fv(VIEW_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.viewMatrix))
        gl.glUniformMatrix4fv(NORMAL_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.normalMatrix))
        gl.glUniformMatrix4fv(PROJECTION_MATRIX_LOCATION, 1, gl.GL_FALSE, concatenate(self.projectionMatrix))

    def setColor(self, color):
        '''
        Send color to fragment shader
        @param color: color
        '''
        gl.glUniform4fv(COLOR_LOCATION, 1, color)

    # For PyPy compatibility
    def cross(self, u, v):
        '''
        Calculate cross production of two vectors
        @param u: first vector
        @param v: second vector
        @return: u x v
        '''
        r = array([0, 0, 0], 'f')
        r[0] = u[1] * v[2] - u[2] * v[1]
        r[1] = u[2] * v[0] - u[0] * v[2]
        r[2] = u[0] * v[1] - u[1] * v[0]
        return r

    def lookAt(self):
        '''
        Calculate view matrix for current camera position, direction and up vector
        @return: view matrix
        '''
        f = normalize(self.cen - self.eye)
        u = normalize(self.up)
        s = normalize(self.cross(f, u))
        u = self.cross(s, f)
        result = identity(4, 'f')
        result[0][0] = s[0]
        result[1][0] = s[1]
        result[2][0] = s[2]
        result[0][1] = u[0]
        result[1][1] = u[1]
        result[2][1] = u[2]
        result[0][2] = -f[0]
        result[1][2] = -f[1]
        result[2][2] = -f[2]
        result[3][0] = -dot(s, self.eye)
        result[3][1] = -dot(u, self.eye)
        result[3][2] = dot(f, self.eye)
        return result

    def perspective(self):
        '''
        Calculate perspective projection matrix
        @return: projection matrix
        '''
        fieldOfView = 45.0
        zNear = 0.1
        zFar = 1000.0
        D2R = pi / 180.0
        yScale = 1.0 / tan(D2R * fieldOfView / 2.0)
        xScale = yScale / self.aspect
        nearmfar = zNear - zFar
        return array(
            [[xScale, 0, 0, 0],
            [0, yScale, 0, 0],
            [0, 0, (zFar + zNear) / nearmfar, -1],
            [0, 0, 2 * zFar * zNear / nearmfar, 0]], 'f')

    def initTexture(self, id, filename):
        '''
        Load texture from file
        @param id: texture id
        @param filename: name of file
        '''
        self.textures[id].load(filename)

    def renderText(self, id, fontname, size, text, color):
        '''
        Render text to texture
        @param id: texture id
        @param fontname: font filename
        @param size: size of characters
        @param text: text
        @param color: text color
        '''
        font = glfont.load_font(fontname, size)
        w, h, data = glfont.render_text(font, text, color, size)
        self.textures[id].load_raw(w, h, data)

    def bindTexture(self, id):
        '''
        Bind texture
        @param id: texture id, if -1 then disable texturing
        '''
        if id == -1 or not self.textures[id].inited:
            gl.glUniform1i(TEXTURE_FLAG_LOCATION, 0)
        else:
            gl.glUniform1i(TEXTURE_FLAG_LOCATION, 1)
            self.textures[id].bind()

    def enableLighting(self):
        '''
        Enable lighting
        '''
        gl.glUniform1i(LIGHTING_FLAG_LOCATION, 1)

    def disableLighting(self):
        '''
        Disable lighting
        '''
        gl.glUniform1i(LIGHTING_FLAG_LOCATION, 0)
