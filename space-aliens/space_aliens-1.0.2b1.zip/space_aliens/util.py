'''
Utility functions.

Author: semicoded.com
Licensed by: BSD 2-Clause License
'''
import os, pygame

class ContinueException(Exception):
    """
    Exit from menu and continue the game.
    """

class ImageLoader():
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        
    def load_image(self, file, convert_alpha=False):
        """
        Load an image and prepare it.
        """
        file = os.path.join(self.data_dir, file)
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit(
                """Could not load image "{}":\n {}
                """.format(file, pygame.get_error())
            )
        if convert_alpha:
            return surface.convert_alpha()
        else:
            return surface.convert()
    
    def load_images(self, *files, convert_alpha=False):
        """
        Repeatedly call load_image(). Returns list.
        """
        imgs = []
        for file in files:
            imgs.append(self.load_image(file, convert_alpha))
        return imgs
    
def save_settings(config, audio, score):
    config["SETTINGS"] = {"sound": audio.sounds,
                          "music": audio.music,
                          "record": score.best}
    with open("config.ini", "w", encoding="utf8") as file:
        config.write(file)

def load_settings(config, audio, score):
    if os.path.isfile("config.ini"):
        config.read("config.ini", encoding="utf8")
        if config["SETTINGS"].getboolean("sound"):
            audio.sounds_on()
        else:
            audio.sounds_off()
        if config["SETTINGS"].getboolean("music"):
            audio.music_on()
        else:
            audio.music_off()
        score.best = int(config["SETTINGS"]["record"])

if __name__ == '__main__':
    loader = ImageLoader("_dd")
    loader.load_image("_invalid_file")