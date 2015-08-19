from game import Game
from gui import GUI
from objectquad import objectQuad
from objectcube import objectCube
from item import *
import OpenGL.GL as gl
from glutils import *
import glfw
from random import *

import gettext
gettext.install("text", "./localization", unicode = 1)


MODE_MENU = 0
MODE_GAME = 1


class Engine:
    '''
    Class Engine works with classes Game and GUI to run and visualize game.
    Also this class gets and process mouse events.
    '''
    def __init__(self, window):
        '''
        Initialize engine
        @param window: main window
        '''
        # Initialize members
        self.window = window
        self.game = None
        self.gui = GUI()
        self.quad = objectQuad()
        self.cube = objectCube()
        self.target = None
        self.target_display_pos = None
        self.runtime = 0.0
        self.cam_dir = array([0, 0, 1], 'f')
        self.cam_up = array([0, 1, 0], 'f')
        self.cam_flag = False
        self.mode = MODE_MENU
        self.menu_items = set()
        # Initialize textures
        self.gui.initTexture(0, "data/item.png")
        self.gui.initTexture(1, "data/aim.png")
        for i in range(10):
            self.gui.renderText(2 + i, "data/mono.ttf", 256, str(i), (255, 255, 255, 255))
        self.gui.renderText(12, "data/mono.ttf", 256, _("STR:"), (255, 255, 255, 255))
        self.gui.renderText(13, "data/mono.ttf", 256, _("DEF:"), (255, 255, 255, 255))
        self.gui.renderText(14, "data/mono.ttf", 256, _("SPD:"), (255, 255, 255, 255))
        self.gui.renderText(15, "data/mono.ttf", 256, _("SHIELD"), (255, 255, 255, 255))
        self.gui.renderText(16, "data/mono.ttf", 256, "+", (255, 255, 255, 255))
        self.gui.renderText(17, "data/mono.ttf", 256, _("NEXT WAVE"), (255, 255, 255, 255))
        self.gui.renderText(18, "data/mono.ttf", 256, ":", (255, 255, 255, 255))
        self.gui.initTexture(19, "data/radar.png")
        self.gui.renderText(20, "data/mono.ttf", 256, _("START"), (255, 255, 255, 255))
        for i in range(1, 8):
            self.gui.initTexture(20 + i, "data/e" + str(i) + ".png")
        # Setup menu
        self.__init_menu()

    def setWindowHeight(self, h):
        '''
        Set window height
        @param h: window height
        '''
        self.gui.setWindowHeight(h)
        # If camera mode on then move cursor to center
        if self.cam_flag:
            glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def setWindowWidth(self, w):
        '''
        Set window width
        @param w: window width
        '''
        self.gui.setWindowWidth(w)
        # If camera mode on the move cursor to center
        if self.cam_flag:
            glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def camera_on(self):
        '''
        Switch on camera mode (only for in game mode)
        '''
        if self.mode == MODE_GAME:
            self.cam_flag = True
            # Hide cursor
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
            # Move cursor to center
            glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def camera_off(self):
        '''
        Switch off camera mode
        '''
        self.cam_flag = False
        # Show cursor
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def camera_switch(self):
        '''
        Switch camera mode
        '''
        if self.cam_flag:
            self.camera_off()
        else:
            self.camera_on()

    def camera_scroll(self, d):
        '''
        Process mouse wheel event
        @param d: wheel rolling direction
        '''
        pass

    def shoot_on(self):
        '''
        Process mouse left down:
        Determine click on buttons or start shooting
        '''
        # In menu determine click on the "START"-button
        if self.mode == MODE_MENU:
            # Convert window coordinates to OpenGL coordinates
            x, y = glfw.get_cursor_pos(self.window)
            x = float(x) / self.gui.getWindowWidth() * 2.0 * self.gui.aspect - self.gui.aspect
            y = 1.0 - float(y) / self.gui.getWindowHeight() * 2.0
            # If button clicked start game
            if x > -1 and x < 1 and y > -0.5 and y < 0.5:
                self.__init_game()
            return
        # In game...
        if self.cam_flag:
            # If camera mode set shooting flag to True
            self.shoot = True
        else:
            # Else determine click on update buttons
            if self.game.getSP():
                # Convert window coordinates to OpenGL coordinates
                x, y = glfw.get_cursor_pos(self.window)
                x = float(x) / self.gui.getWindowWidth() * 2.0 * self.gui.aspect - self.gui.aspect
                y = 1.0 - float(y) / self.gui.getWindowHeight() * 2.0
                # Update power button
                if x > - self.gui.aspect + 0.6 and x < - self.gui.aspect + 0.7 and y > 0.8 and y < 0.9:
                    if self.game.getMainPlayer().getPower() < 10:
                        self.game.getMainPlayer().addPower(1)
                        self.game.decSP()
                # Update defence button
                if x > - self.gui.aspect + 0.6 and x < - self.gui.aspect + 0.7 and y > 0.65 and y < 0.75:
                    if self.game.getMainPlayer().getDefence() < 10:
                        self.game.getMainPlayer().addDefence(1)
                        self.game.decSP()
                # Update speed button
                if x > - self.gui.aspect + 0.6 and x < - self.gui.aspect + 0.7 and y > 0.5 and y < 0.6:
                    if self.game.getMainPlayer().getSpeed() < 10:
                        self.game.getMainPlayer().addSpeed(1)
                        self.game.decSP()

    def shoot_off(self):
        '''
        Process mouse left up:
        Stop shooting
        '''
        self.shoot = False

    def __init_menu(self):
        '''
        Initialize menu mode
        '''
        # Free game and switch off camera mode
        self.game = None
        self.camera_off()
        self.mode = MODE_MENU

    def __init_game(self):
        '''
        Initialize game
        '''
        # Create Game object, initialize side variables
        self.game = Game(self)
        self.target = None
        self.target_display_pos = None
        self.shoot = False
        self.cam_dir = array([0, 0, 1], 'f')
        self.cam_up  = array([0, 1, 0], 'f')
        self.cam_flag = False
        self.mode = MODE_GAME
        self.camera_on()

    def defeat(self):
        '''
        Process game defeat:
        Return to main menu
        '''
        self.__init_menu()

    def __process_camera(self):
        '''
        Calculate camera rotation caused by mouse moving
        '''
        x, y = glfw.get_cursor_pos(self.window)
        dx = x - self.gui.window_width / 2.0
        dy = y - self.gui.window_height / 2.0
        cam_dir = v4_v3(mul_v(rotate(-dy * 0.5, cross(self.cam_dir, self.cam_up)), v3_v4(self.cam_dir)))
        cam_up  = v4_v3(mul_v(rotate(-dy * 0.5, cross(self.cam_dir, self.cam_up)), v3_v4(self.cam_up)))
        cam_dir = v4_v3(mul_v(rotate(-dx * 0.5, cam_up), v3_v4(cam_dir)))
        self.cam_dir = normalize(cam_dir)
        self.cam_up  = normalize(cam_up)
        glfw.set_cursor_pos(self.window, self.gui.window_width / 2, self.gui.window_height / 2)

    def __clear_screen(self):
        '''
        Clear screen, setup viewport
        '''
        gl.glClearColor(0.05, 0.05, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glViewport(0, 0, self.gui.window_width, self.gui.window_height)

    def __init_game_3d(self):
        '''
        Calculate projection and view matrices according to camera position and direction
        '''
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.gui.projectionMatrix = self.gui.perspective()
        self.gui.eye = self.game.getMainPlayer().getPosition()
        self.gui.cen = self.gui.eye + self.cam_dir
        self.gui.up  = self.cam_up
        self.gui.viewMatrix = self.gui.lookAt()

    def __init_menu_3d(self):
        '''
        Calculate projection and view matrices for menu rendering
        '''
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.gui.projectionMatrix = self.gui.perspective()
        self.gui.eye = array([0, 0, 0], 'f')
        self.gui.cen = array([0, 0, 1], 'f')
        self.gui.up  = array([0, 1, 0], 'f')
        self.gui.viewMatrix = self.gui.lookAt()

    def __draw_enemies(self):
        '''
        Draw all game enemies
        '''
        # Enable lighting
        self.gui.enableLighting()
        # Draw enemies
        for i in self.game.getEnemies():
            # Calculate model matrix
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                scale(array([3, 3, 3], 'f')))
            self.gui.sendMatrices()
            # If enemy is current target then color is red else color is green
            # Also save for target it's display position to render additional information
            if i == self.target:
                self.target_display_pos = v4_v3(mul_v(self.gui.projectionMatrix,
                    mul_v(self.gui.viewMatrix, v3_v4(i.getPosition()))))
            # Set color and texture
            self.gui.setColor(array([1, 1, 1, 1], 'f'))
            self.gui.bindTexture(20 + i.getTexture())
            # And draw!
            self.cube.draw()
        # Disable lighting
        self.gui.disableLighting()

    def __draw_items(self):
        '''
        Draw flying red, green and blue items
        '''
        # Setup texture
        self.gui.bindTexture(0)
        # Sort items for right alpha channel blending
        free_items = sorted(self.game.getFreeItems(), cmp=comparer(self.gui.eye))
        # Draw items
        for i in free_items:
            # Find rotation angle and axis to item's plane will be orthogonal to camera direction
            pos_dir = normalize(i.getPosition() - self.gui.eye)
            base_dir = array([0, 0, 1], 'f')
            if abs(dot(base_dir, pos_dir)) > 1 - (10.0 ** -5):
                rot_axis = array([0, 1, 0], 'f')
                if dot(base_dir, pos_dir) > 0:
                    rot_angle = 0
                else:
                    rot_angle = 180
            else:
                rot_axis = cross(pos_dir, base_dir)
                rot_angle = 180 - 180 * arccos(dot(pos_dir, base_dir)) / pi
            # Calculate model matrix
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                rotate(rot_angle, rot_axis))
            self.gui.sendMatrices()
            # Determine color
            if i.getColor() == COLOR_RED:
                self.gui.setColor(array([1, 0, 0, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_BLUE:
                self.gui.setColor(array([0, 0, 1, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_GREEN:
                self.gui.setColor(array([0, 1, 0, i.getLifetime()], 'f'))
            # Draw it!
            self.quad.draw()

    def __draw_bulls(self):
        '''
        Draw bullets
        '''
        # Setup texture
        self.gui.bindTexture(0)
        # Draw all bullets as well as items draw
        for i in sorted(self.game.getBulls(), cmp=comparer(self.gui.eye)):
            pos_dir = normalize(i.getPosition() - self.gui.eye)
            base_dir = array([0, 0, 1], 'f')
            if abs(dot(base_dir, pos_dir)) > 1 - (10.0 ** -5):
                rot_axis = array([0, 1, 0], 'f')
                if dot(base_dir, pos_dir) > 0:
                    rot_angle = 0
                else:
                    rot_angle = 180
            else:
                rot_axis = cross(pos_dir, base_dir)
                rot_angle = 180 - 180 * arccos(dot(pos_dir, base_dir)) / pi
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                rotate(rot_angle, rot_axis))
            self.gui.setColor(array([1, 0, 0, 1], 'f'))
            self.gui.sendMatrices()
            self.quad.draw()

    def __init_2d(self):
        '''
        Calculate projection and view matrix for 2D rendering
        '''
        gl.glDisable(gl.GL_DEPTH_TEST)
        self.gui.projectionMatrix = identity(4, 'f')
        self.gui.viewMatrix = scale(array([1.0 / self.gui.aspect, 1, 1], 'f'))

    def __draw_target_stats(self):
        '''
        Draw target's stats such as power, defence and speed
        @return:
        '''
        # Convert stats to strings
        str_str = str(self.target.getPower())
        def_str = str(self.target.getDefence())
        spd_str = str(self.target.getSpeed())
        # Calculate model matrix
        self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect - 0.125
            - (len(str_str) + len(def_str) + len(spd_str)) * 0.025,
            self.target_display_pos[1] + 0.15, 0], 'f')),
            scale(array([0.05, 0.1, 0.1], 'f')))
        # Draw power counter
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        for i in str_str:
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([0.05, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Draw defence counter
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        for i in def_str:
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([0.05, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Draw speed counter
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        for i in spd_str:
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([0.05, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()

    def __draw_target_health(self):
        '''
        Draw target's health bar
        '''
        # Disable texturing
        self.gui.bindTexture(-1)
        # Calculate model matrix for back bar
        self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect,
            self.target_display_pos[1] + 0.2, 0], 'f')),
            scale(array([0.4, 0.025, 1], 'f')))
        self.gui.sendMatrices()
        # Draw back bar
        self.gui.setColor(array([0, 0, 0.25, 1], 'f'))
        self.quad.draw()
        # Calculate model matrix for front bar
        self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect + 0.2 *
            (self.target.getHealth() - 1.0), self.target_display_pos[1] + 0.2, 0], 'f')),
            scale(array([0.4 * self.target.getHealth(), 0.025, 1], 'f')))
        self.gui.sendMatrices()
        # Draw front bar
        self.gui.setColor(array([0, 0, 1.0, 1], 'f'))
        self.quad.draw()

    def __draw_aim(self):
        '''
        Draw aim
        '''
        self.gui.bindTexture(1)
        self.gui.modelMatrix = scale(array([0.2, 0.2, 0.2], 'f'))
        self.gui.sendMatrices()
        # If target draw red aim else draw white aim
        if self.target:
            self.gui.setColor(array([1, 0, 0, 1], 'f'))
        else:
            self.gui.setColor(array([1, 1, 1, 1], 'f'))
        self.quad.draw()
        # Also draw aim on the target
        if self.target:
            self.gui.modelMatrix = mul(translate(array([self.target_display_pos[0] * self.gui.aspect,
                self.target_display_pos[1], 0], 'f')),
                scale(array([0.2, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.quad.draw()

    def __draw_item_icons(self):
        '''
        Draw item icons at top right position of the screen
        '''
        # Draw red item icon
        self.gui.bindTexture(0)
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.1, 0.85, 0], 'f')),
            scale(array([0.2, 0.2, 0.2], 'f')))
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.quad.draw()
        # Draw blue item icon
        self.gui.bindTexture(0)
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.1, 0.7, 0], 'f')),
            scale(array([0.2, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        self.gui.sendMatrices()
        self.quad.draw()
        # Draw green item icon
        self.gui.bindTexture(0)
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.1, 0.55, 0], 'f')),
            scale(array([0.2, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.quad.draw()

    def __draw_item_count(self):
        '''
        Draw item counters near item icons
        '''
        # Draw red item count
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.15, 0.85, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        for i in reversed(str(self.game.getMainPlayer().getRedItems())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Draw blue item count
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.15, 0.7, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        for i in reversed(str(self.game.getMainPlayer().getBlueItems())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Draw green item count
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect - 0.15, 0.55, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        for i in reversed(str(self.game.getMainPlayer().getGreenItems())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()

    def __draw_player_stats(self):
        '''
        Draw player stats such as power, defence and speed
        '''
        # Draw power
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.2, 0.85, 0], 'f')),
            scale(array([0.4, 0.2, 0.2], 'f')))
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.gui.bindTexture(12)
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect +
                0.5 + 0.1 * len(str(self.game.getMainPlayer().getPower())), 0.85, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
        for i in reversed(str(self.game.getMainPlayer().getPower())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Draw defence
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.2, 0.7, 0], 'f')),
            scale(array([0.4, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 0, 1, 1], 'f'))
        self.gui.sendMatrices()
        self.gui.bindTexture(13)
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect +
                0.5 + 0.1 * len(str(self.game.getMainPlayer().getDefence())), 0.7, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
        for i in reversed(str(self.game.getMainPlayer().getDefence())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()
        # Draw speed
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.2, 0.55, 0], 'f')),
            scale(array([0.4, 0.2, 0.2], 'f')))
        self.gui.setColor(array([0, 1, 0, 1], 'f'))
        self.gui.sendMatrices()
        self.gui.bindTexture(14)
        self.quad.draw()
        self.gui.modelMatrix = mul(translate(array([- self.gui.aspect +
                0.5 + 0.1 * len(str(self.game.getMainPlayer().getSpeed())), 0.55, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
        for i in reversed(str(self.game.getMainPlayer().getSpeed())):
            self.gui.bindTexture(int(i) + 2)
            self.gui.modelMatrix = mul(translate(array([-0.1, 0, 0], 'f')), self.gui.modelMatrix)
            self.gui.sendMatrices()
            self.quad.draw()

    def __draw_update_buttons(self):
        '''
        Draw update buttons near player stats
        '''
        self.gui.bindTexture(16)
        # Draw update power button
        if self.game.getMainPlayer().getPower() < 10:
            self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.65, 0.85, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.gui.setColor(array([1, 0, 0, sin(10 * self.runtime) * 0.25 + 0.75], 'f'))
            self.quad.draw()
        # Draw update defence button
        if self.game.getMainPlayer().getDefence() < 10:
            self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.65, 0.7, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.gui.setColor(array([0, 0, 1, sin(10 * self.runtime) * 0.25 + 0.75], 'f'))
            self.quad.draw()
        # Draw update speed button
        if self.game.getMainPlayer().getSpeed() < 10:
            self.gui.modelMatrix = mul(translate(array([- self.gui.aspect + 0.65, 0.55, 0], 'f')),
                scale(array([0.1, 0.2, 0.2], 'f')))
            self.gui.sendMatrices()
            self.gui.setColor(array([0, 1, 0, sin(10 * self.runtime) * 0.25 + 0.75], 'f'))
            self.quad.draw()

    def __draw_player_health(self):
        '''
        Draw player's health bar at bottom of the screen
        '''
        # Disable texturing
        self.gui.bindTexture(-1)
        # Draw back bar
        self.gui.modelMatrix = mul(translate(array([0, -1 + 0.05, 0], 'f')),
            scale(array([2 * self.gui.aspect, 0.1, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 0.25, 1], 'f'))
        self.quad.draw()
        # Draw front bar
        self.gui.modelMatrix = mul(translate(array([self.gui.aspect *
            (self.game.getMainPlayer().getHealth() - 1.0), -1 + 0.05, 0], 'f')),
            scale(array([2 * self.gui.aspect * self.game.getMainPlayer().getHealth(), 0.1, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([0, 0, 1.0, 1], 'f'))
        self.quad.draw()
        # Draw text ("SHIELD" for english) on the bar
        self.gui.bindTexture(15)
        self.gui.modelMatrix = mul(translate(array([0, -1 + 0.05, 0], 'f')),
            scale(array([0.3, 0.1, 1], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([1.0, 1.0, 1.0, 1], 'f'))
        self.quad.draw()

    def __draw_wave_timer(self, time):
        '''
        Draw wave timer
        @param time: remaining time
        '''
        # Draw text ("NEXT WAVE" for english)
        self.gui.bindTexture(17)
        self.gui.modelMatrix = mul(translate(array([0, 0.85, 0], 'f')),
            scale(array([1.0, 0.2, 0.2], 'f')))
        self.gui.sendMatrices()
        self.gui.setColor(array([1.0, 1.0, 0.0, 1], 'f'))
        self.quad.draw()
        # Determine four digits for MM:SS format
        if time < 0:
            time_s = 0
            time_m = 0
        else:
            time_s = (int(time) + 1) % 60
            time_m = (int(time) + 1) / 60
        time_s1 = time_s / 10
        time_s2 = time_s % 10
        time_m1 = time_m / 10
        time_m2 = time_m % 10
        # Draw digits and ':'-delimiter
        self.gui.modelMatrix = mul(translate(array([-0.25, 0.65, 0], 'f')),
            scale(array([0.1, 0.2, 0.2], 'f')))
        self.gui.bindTexture(2 + time_m1)
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        self.gui.sendMatrices()
        self.quad.draw()
        self.gui.bindTexture(2 + time_m2)
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        self.gui.sendMatrices()
        self.quad.draw()
        self.gui.bindTexture(18)
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        self.gui.sendMatrices()
        self.quad.draw()
        self.gui.bindTexture(2 + time_s1)
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        self.gui.sendMatrices()
        self.quad.draw()
        self.gui.bindTexture(2 + time_s2)
        self.gui.modelMatrix = mul(translate(array([0.1, 0, 0], 'f')), self.gui.modelMatrix)
        self.gui.sendMatrices()
        self.quad.draw()

    def __draw_radar(self):
        '''
        Draw enemy radar
        '''
        view = self.gui.lookAt()
        self.gui.bindTexture(19)
        self.gui.setColor(array([1, 0, 0, 1], 'f'))
        for i in self.game.getEnemies():
            pos = normalize(v4_v3(mul_v(view, v3_v4(i.getPosition()))))
            if pos[2] < -0.9:
                continue
            angle = arctan2(pos[1], pos[0])
            if angle > pi / 4:
                if angle < 3 * pi / 4:
                    self.gui.modelMatrix = translate(array([cos(angle) * self.gui.aspect, 1 - 0.04, 0], 'f'))
                else:
                    self.gui.modelMatrix = translate(array([-self.gui.aspect + 0.04, sin(angle), 0], 'f'))
            else:
                if angle > - pi / 4:
                    self.gui.modelMatrix = translate(array([self.gui.aspect - 0.04, sin(angle), 0], 'f'))
                else:
                    if angle < - 3 * pi / 4:
                        self.gui.modelMatrix = translate(array([-self.gui.aspect + 0.04, sin(angle), 0], 'f'))
                    else:
                        self.gui.modelMatrix = translate(array([cos(angle) * self.gui.aspect, -1 + 0.04, 0], 'f'))
            self.gui.modelMatrix = mul(self.gui.modelMatrix, scale(array([0.1, 0.1, 0.1], 'f')))
            self.gui.sendMatrices()
            self.quad.draw()

    def __process_menu_items(self, elapsedTime):
        '''
        Process menu's flying item moving
        @param elapsedTime: elapsed time
        @return:
        '''
        # Add items
        while len(self.menu_items) < 20:
            # Set random color
            r = randint(0, 2)
            clr = COLOR_RED
            if r == 1:
                clr = COLOR_BLUE
            if r == 2:
                clr = COLOR_GREEN
            # Set random location
            rx = (random() * 2.0 - 1.0) * 25.0
            ry = (random() * 2.0 - 1.0) * 25.0
            rz = 100.0 * (1 + random())
            self.menu_items.add(Item(array([rx, ry, rz], 'f'), clr, 1))
        # Delete items which locate behind the screen
        td = []
        for i in self.menu_items:
            i.getPosition()[2] -= elapsedTime * 100.0
            if i.getPosition()[2] < 0:
                td.append(i)
        for i in td:
            self.menu_items.remove(i)

    def __draw_menu_items(self):
        '''
        Draw menu's flying red, green and blue items
        '''
        # Disable texturing
        self.gui.bindTexture(0)
        # Sort items to right alpha channel blending
        mi = sorted(self.menu_items, cmp=comparer(array([0, 0, 0], 'f')))
        # Draw flying items
        for i in mi:
            pos_dir = normalize(i.getPosition())
            base_dir = array([0, 0, 1], 'f')
            if abs(dot(base_dir, pos_dir)) > 1 - (10.0 ** -5):
                rot_axis = array([0, 1, 0], 'f')
                if dot(base_dir, pos_dir) > 0:
                    rot_angle = 0
                else:
                    rot_angle = 180
            else:
                rot_axis = cross(pos_dir, base_dir)
                rot_angle = 180 - 180 * arccos(dot(pos_dir, base_dir)) / pi
            self.gui.modelMatrix = mul(translate(i.getPosition()),
                rotate(rot_angle, rot_axis))
            self.gui.sendMatrices()
            if i.getColor() == COLOR_RED:
                self.gui.setColor(array([1, 0, 0, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_BLUE:
                self.gui.setColor(array([0, 0, 1, i.getLifetime()], 'f'))
            if i.getColor() == COLOR_GREEN:
                self.gui.setColor(array([0, 1, 0, i.getLifetime()], 'f'))
            self.quad.draw()

    def __menu_draw_start(self):
        '''
        Draw "START"-button
        '''
        self.gui.modelMatrix = scale(array([2, 1, 1], 'f'))
        self.gui.setColor(array([1, 1, 0, sin(10 * self.runtime) * 0.25 + 0.75], 'f'))
        self.gui.bindTexture(20)
        self.gui.sendMatrices()
        self.quad.draw()

    def __menu_step(self, elapsedTime):
        '''
        Process time slice for menu mode
        @param elapsedTime: elapsed time
        '''
        self.__process_menu_items(elapsedTime)
        self.__clear_screen()
        self.__init_menu_3d()
        self.__draw_menu_items()
        self.__init_2d()
        self.__menu_draw_start()

    def __game_step(self, elapsedTime):
        '''
        Process time slice for game mode
        @param elapsedTime: elapsed time
        @return:
        '''
        # Move player
        self.game.move(elapsedTime, self.cam_dir)
        # Process game logic
        self.game.process(elapsedTime)
        # If defeat return
        if not self.game:
            return
        # Process camera rotation
        if self.cam_flag:
            self.__process_camera()
        # Determine target if there is
        self.target = None
        for i in self.game.getEnemies():
            dst = dist(i.getPosition(), self.game.getMainPlayer().getPosition())
            if dst > 10000:
                continue
            ang = dot(self.cam_dir, normalize(i.getPosition() - self.game.getMainPlayer().getPosition()))
            if ang < 0.99:
                continue
            if not self.target:
                self.target = i
                ang_old = ang
            else:
                if ang > ang_old:
                    self.target = i
                    ang_old = ang
        # Process shooting
        if self.shoot and self.target:
            self.game.shoot(self.target, self.cam_up)
        # Render game
        self.__clear_screen()
        self.__init_game_3d()
        self.__draw_enemies()
        self.__draw_items()
        self.__draw_bulls()
        self.__init_2d()
        if self.target:
            self.__draw_target_stats()
            self.__draw_target_health()
        self.__draw_aim()
        self.__draw_item_icons()
        self.__draw_item_count()
        self.__draw_player_stats()
        if self.game.getSP():
            self.__draw_update_buttons()
        self.__draw_player_health()
        if self.game.getWaveTimerFlag():
            self.__draw_wave_timer(self.game.getWaveTimerTime())
        self.__draw_radar()

    def step(self, elapsedTime):
        '''
        Process time slice
        @param elapsedTime: elapsed time
        '''
        self.runtime += elapsedTime
        if self.mode == MODE_MENU:
            self.__menu_step(elapsedTime)
        if self.mode == MODE_GAME:
            self.__game_step(elapsedTime)
