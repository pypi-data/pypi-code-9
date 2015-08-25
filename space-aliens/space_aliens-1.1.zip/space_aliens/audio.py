'''
Audio for space_aliens.

Author: semicoded.com
Licensed by: BSD 2-Clause License
'''
import os, pygame

class DummySound:
    def play(self): pass

def load_sound(*file_path):
    """
    *file_path -- eg. ["data", "sounds", "cheese.png"]
    """
    file = os.path.join(*file_path)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        raise SystemExit('Warning, unable to load, %s' % file)

class Audio():
    """
    Class for playing audio.
    Class needs to be initialized
    after Pygame (is initialized).
    
    on -- True -> on, False -> off
    """
    # default values
    music = True
    sounds = True

    @classmethod
    def init(cls, data_dir):
        cls.boom_sound = load_sound(data_dir, "boom.wav")
        cls.shoot_sound = load_sound(data_dir, "flaunch.wav")
        cls.bg_music = os.path.join(data_dir, "fast_bg.ogg")
        cls.menu_music = os.path.join(data_dir, "slow_bg.ogg")
        cls.dummy = DummySound()
    
    def music_on(self):
        """
        Turn background music on.
        """
        self.music = True
    
    def music_off(self):
        """
        Turn background music off.
        """
        self.music = False
        pygame.mixer.music.stop()
        
    def sounds_on(self):
        """
        Turn sounds (eg. explosions) on.
        """
        # just an indicator
        self.sounds = True
        self.boom_sound = Audio.boom_sound
        self.shoot_sound = Audio.shoot_sound
    
    def sounds_off(self):
        """
        Turn sounds (eg. explosions) on.
        """
        # just an indicator
        self.sounds = False
        self.boom_sound = Audio.dummy
        self.shoot_sound = Audio.dummy
    
    def play_menu(self):
        """
        Play background menu music.
        Does nothing if music is off.
        """
        if self.music:
            pygame.mixer.music.load(self.menu_music)
            pygame.mixer.music.play(-1)
    
    def play_bg(self):
        """
        Play background game music.
        Does nothing if music is off.
        """
        if self.music:
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.play(-1)
            
    def play_shoot(self):
        """
        Play shoot sound.
        Does nothing if sounds are off.
        """
        self.shoot_sound.play()
        
    def play_boom(self):
        """
        Play explosion sound.
        Does nothing if sounds are off.
        """
        self.boom_sound.play()