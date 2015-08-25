'''
Game menu for space_aliens.

Author: semicoded.com
Licensed by: BSD 2-Clause License
'''
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, Color
from .util import ContinueException, ImageLoader

class ButtonGroup():
    """
    Group of Button(s).
    """
    def __init__(self):
        self.btns = []
        
        
    def add_btn(self, btn):
        """
        btn -- Button
        """
        self.btns.append(btn)
    
    def get_all(self):
        """
        Return Button(s).
        """
        return self.btns
    
    def hover(self, x, y):
        """
        Call hover() on any Button in this group that
        contains position (x, y).
        """
        for btn in self.btns:
            btn.surf = btn.orig
            if btn.rect.collidepoint(x, y):
                btn.surf = btn.hover_surf
        
    def click(self, x, y):
        """
        Call click() on any Button in this group that
        contains position (x, y).
        """
        for btn in self.btns:
            btn.surf = btn.orig
            if btn.rect.collidepoint(x, y):
                btn.click(btn)
            
class Button():
    """
    Button for clicking.
    You need to add it to ButtonGroup to register
    clicks/hovering. See ButtonGroup for more.
    All Surfaces (on one Button) need to have uniform size
    (there is only one rect).
    
    surf -- Surface
    hover_surf -- Surface when hovered over by mouse
    click -- function called on click
    """
    def __init__(self, surf, hover_surf=None, click=None):
        self.change_surf(surf)
        self.rect = surf.get_rect()
        if hover_surf is not None:
            self.hover_surf = hover_surf
        if click is None:
            click = self._dummy
        self.click = click
        
    def change_surf(self, new_surf):
        """
        Change Surface. Changes only Surface (not rect
        not anything else).
        """
        self.surf = new_surf
        self.orig = new_surf
        self.hover_surf = new_surf
    
    def _dummy(self, *anything):
        """
        Do nothing.
        """

class GameMenu():
    menu_fps = 10
    """
    Provides game menu functionality.
    """
    def __init__(self, screen, font, audio,
                 bg_image, exit_fnc, data_dir):
        self.screen_rect = screen.get_rect()
        self.screen = screen
        self.audio = audio
        self.bg_image = bg_image
        self._exit = exit_fnc
        
        self.menu_surf = pygame.Surface(self.screen_rect.size)
        self.menu_surf.set_alpha(128)
        self.menu_surf.fill(Color("black"))
        
        offset = self.screen_rect.h/6
        self.start_btns = ButtonGroup()
        self.resume_btns = ButtonGroup()
        
        surf = font.render("START", True, Color("white"))
        hover = font.render("START", True, Color("red"))
        start = Button(surf, hover, click=self._continue)
        start.rect.centerx = self.screen_rect.centerx
        start.rect.top = offset
        self.start_btns.add_btn(start)
        
        surf = font.render("RESUME", True, Color("white"))
        hover = font.render("RESUME", True, Color("red"))
        resume = Button(surf, hover, click=self._continue)
        resume.rect.centerx = self.screen_rect.centerx
        resume.rect.top = offset
        self.resume_btns.add_btn(resume)
        
        
        surf = font.render("Music: ", True, Color("white"))
        music = Button(surf)
        music.rect.top = start.rect.bottom
        music.rect.centerx = start.rect.centerx
        self.start_btns.add_btn(music)
        self.resume_btns.add_btn(music)
        
        loader = ImageLoader(data_dir)
        
        size = surf.get_rect().height
        img = loader.load_image("sound_on.png", True)
        img = pygame.transform.smoothscale(img, (size, size))
        self.on_image = img
        
        size = surf.get_rect().height
        img = loader.load_image("sound_off.png", True)
        img = pygame.transform.smoothscale(img, (size, size))
        self.off_image = img
        
        img = self.on_image if self.audio.music else self.off_image
        music_control = Button(img, click=self._switch_music)
        music_control.rect.left = music.rect.right
        music_control.rect.top = music.rect.top
        self.start_btns.add_btn(music_control)
        self.resume_btns.add_btn(music_control)
        
        surf = font.render("Sounds: ", True, Color("white"))
        sounds = Button(surf)
        sounds.rect.top = music.rect.bottom
        sounds.rect.centerx = start.rect.centerx
        self.start_btns.add_btn(sounds)
        self.resume_btns.add_btn(sounds)
        
        img = self.on_image if self.audio.sounds else self.off_image
        sounds_control = Button(img, click=self._switch_sounds)
        sounds_control.rect.left = sounds.rect.right
        sounds_control.rect.top = sounds.rect.top
        self.start_btns.add_btn(sounds_control)
        self.resume_btns.add_btn(sounds_control)
        
        surf = font.render("Authors", True, Color("white"))
        hover = font.render("Authors", True, Color("red"))
        authors = Button(surf, hover, 
                          click=self._authors)
        authors.rect.centerx = self.screen_rect.centerx
        authors.rect.top = sounds.rect.bottom
        self.start_btns.add_btn(authors)
        self.resume_btns.add_btn(authors)
        
        surf = font.render("Exit", True, Color("white"))
        hover = font.render("Exit", True, Color("red"))
        exit_btn = Button(surf, hover, 
                          click=self._exit_game)
        exit_btn.rect.centerx = self.screen_rect.centerx
        exit_btn.rect.top = authors.rect.bottom
        self.start_btns.add_btn(exit_btn)
        self.resume_btns.add_btn(exit_btn)
        
    @staticmethod
    def _continue(btn):
        raise ContinueException
    
    
    def _switch_sounds(self, btn):
        if self.audio.sounds:
            self.audio.sounds_off()
            btn.change_surf(self.off_image)
        else:
            self.audio.sounds_on()
            btn.change_surf(self.on_image)
    
    def _switch_music(self, btn):
        if self.audio.music:
            self.audio.music_off()
            btn.change_surf(self.off_image)
        else:
            self.audio.music_on()
            self.audio.play_menu()
            btn.change_surf(self.on_image)
    
    def _exit_game(self, btn):
        self._exit()
    
    def _authors(self, btn):
        self.show_authors()
        self.screen.blit(self.bg_image, (0, 0), self.screen_rect)
        self.screen.blit(self.menu_surf, (0, 0), self.screen_rect)
        pygame.display.update()
    
    def show_authors(self):
#         self.screen.blit(self.menu_surf, (0, 0))
        self.screen.fill(Color("black"))
        clock = pygame.time.Clock()
        
        font = pygame.font.Font("data/freesansbold.ttf", 20)
        color = Color("white")
        
        msgs = [
            'code: semicoded.com',
            'Licensed by: BSD 2-Clause License',
            '',
            'cruiser enemy: http://millionthvector.blogspot.de',
            'Licensed by: CC BY 4.0',
            '',
            '"boom" sound: http://opengameart.org/users/dklon',
            'Licensed by: CC BY 3.0',
            '',
            '"shoot" sound: Michel Baradari apollo-music.de',
            'Licensed by: CC BY 3.0'
        ]
        y = self.screen_rect.h/10
        for msg in msgs:
            text = font.render(msg, True, Color("white"))
            rect = text.get_rect(centerx=self.screen_rect.centerx, top=y)
            y += rect.h
            self.screen.blit(text, rect)
        rect.bottom += rect.h
        
        msg = "Press any key to return."
        info_surf = font.render(msg, True, color)
        info_rect = info_surf.get_rect(midtop=rect.midbottom)
        self.screen.blit(info_surf, info_rect)
        
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._exit()
                elif event.type == KEYDOWN:
                    return
                
            # cap framerate
            clock.tick(GameMenu.menu_fps)
        
    
    def show_menu(self, resume=True, clear=False):
        """
        Show menu and handle input.
        
        resume -- controls resume/start Button's text
        clear -- if True background will be cleaned
        """
        self.audio.play_menu()
        if clear:
            self.screen.blit(self.bg_image, (0, 0), self.screen_rect)
            pygame.display.update()
            
        self.screen.blit(self.menu_surf, (0, 0))
        clock = pygame.time.Clock()
        
        btns = self.resume_btns if resume else self.start_btns
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        raise ContinueException
                    elif event.key == K_SPACE:
                        raise ContinueException
                elif event.type == pygame.MOUSEMOTION:
                    btns.hover(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    btns.click(*event.pos)
                

            for btn in btns.get_all():
                self.screen.blit(btn.surf, btn.rect)
            pygame.display.update()
                
            # cap framerate
            clock.tick(GameMenu.menu_fps)
            
    def show_score(self, score):
        """
        score -- Score
        """
        self.screen.blit(self.menu_surf, (0, 0))
        clock = pygame.time.Clock()
        
        font = pygame.font.Font("data/freesansbold.ttf", 32)
        msg = "Score: {}".format(score.score)
        score_surf = font.render(msg, True, Color("white"))
        score_rect = score_surf.get_rect(bottom=self.screen_rect.centery,
                                         centerx=self.screen_rect.centerx)
        self.screen.blit(score_surf, score_rect)
        
        if score.score > score.best:
            msg = "NEW HIGHSCORE!"
            color = Color("red")
            
            score.best = score.score
        else:
            msg = "Highscore: {}".format(score.best)
            color = Color("white")
        high_surf = font.render(msg, True, color)
        high_rect = high_surf.get_rect(midtop=score_rect.midbottom)
        self.screen.blit(high_surf, high_rect)
        
        msg = "Press any key to continue."
        info_surf = font.render(msg, True, Color("white"))
        info_rect = info_surf.get_rect(midtop=high_rect.midbottom)
        self.screen.blit(info_surf, info_rect)
        
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._exit()
                elif event.type == KEYDOWN:
                    return
                
            # cap framerate
            clock.tick(GameMenu.menu_fps)