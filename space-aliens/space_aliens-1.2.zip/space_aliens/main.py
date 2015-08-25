'''
Space shooter. With aliens. From SPACE!
Powered by Pygame.

If you change FPS it should work but eg. enemy speed
will probably be too slow/fast.

Do not use pygame.font.Font(None, whatever) - use
"data/freesansbold.ttf". The font is not included when
freezing so I included it manually.

Author: semicoded.com
Licensed by: BSD 2-Clause License
'''
import os, random, pygame, sys
from pygame.locals import (
    Rect, K_d, K_a, K_LEFT, K_RIGHT, QUIT, KEYDOWN, K_ESCAPE, 
    K_SPACE, Color
    )
from configparser import ConfigParser
from space_aliens.menu import GameMenu
from space_aliens.audio import Audio
from space_aliens.util import (
    ImageLoader, ContinueException, save_settings, load_settings
    )

global_speed = 10
# tested with 30 FPS
fps = 30
config = ConfigParser()


class Player(pygame.sprite.Sprite):
    """
    Player.
    """
    images = []
    speed = global_speed
    max_shots = 2
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=screen_rect.midbottom)
        self.reloading = 0
        self.shield = None

    def move(self, direction):
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(screen_rect)
        self.image = self.images[direction + 1]

    def gunpos(self):
        return self.rect.centerx, self.rect.top
    
class Alien(pygame.sprite.Sprite):
    """
    Basic enemy.
    """
    images = []
    speed = global_speed
    bomb_odds = 0.03
    # change per alive bomb
    odds_change = 0.01
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1,1))
        if self.facing < 0:
            self.rect.right = screen_rect.right
    
    def update(self):
        self.rect.move_ip(Alien.speed * self.facing, 0)
        if not screen_rect.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(screen_rect)

class Cruiser(pygame.sprite.Sprite):
    """
    Medium enemy.
    """
    images = []
    speed = global_speed
    # how often it recomputes direction
    dir_period = fps
    # how often it appears (every nth enemy)
    entry_period = 10
    bomb_period = fps
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.dir_period = Cruiser.dir_period
        self.facing = random.choice((-1,1))
        self.bomb_period = Cruiser.bomb_period
        if self.facing < 0:
            self.rect.right = screen_rect.right
        
    def update(self):
        if self.bomb_period == 0:
            Bomb(self)
            self.bomb_period = Cruiser.bomb_period
        else:
            self.bomb_period -= 1
        
        if self.dir_period == 0:
            self.facing = random.choice((-1,1))
            self.dir_period = Cruiser.dir_period
        else:
            self.dir_period -= 1
        self.rect.move_ip(Cruiser.speed * self.facing, 0)
        
        if not screen_rect.contains(self.rect):
            self.facing = -self.facing
#             self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(screen_rect)
        
            
class Shot(pygame.sprite.Sprite):
    """
    Missile. Goes up and kills enemies.
    """
    speed = -global_speed * 1.5
    images = []
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        audio.play_shoot()
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:
            self.kill()
            
class Bomb(pygame.sprite.Sprite):
    """
    Missile. Goes down and kills Player.
    """
    speed = global_speed * 1.5
    images = []
    def __init__(self, alien):
        pygame.sprite.Sprite.__init__(self, self.containers)
        audio.play_shoot()
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=
                    alien.rect.midbottom)
        Alien.bomb_odds -= Alien.odds_change

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > screen_rect.bottom:
            self.kill()
            
    def kill(self):
        """
        kill() is overridden to update Alien.bomb_odds
        """
        super().kill()
        Alien.bomb_odds += Alien.odds_change
    
class Explosion(pygame.sprite.Sprite):
    """
    BOOM!
    """
    default_life = 15
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        audio.play_boom()
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.rect.move_ip(0, -self.rect.h//4)
        self.life = Explosion.default_life

    def update(self):
        self.life = self.life - 1
        # from 0016.png to last image
        self.image = self.images[-self.life]
        if self.life <= 0: self.kill()
        
class BigExplosion(Explosion):
    """
    Bigger BOOM.
    """
    images = []
    def __init__(self, actor):
        Explosion.__init__(self, actor)
        
    @classmethod
    def set_and_scale_images(cls, imgs):
        for img in imgs:
            BigExplosion.images.append(pygame.transform.scale2x(img))
 
def load_expl_images(img_loader):
    """
    Load images for explosion animation.
    """
    imgs = []
    for x in range(16, 31):
        img_path = os.path.join("explosion_red", "{:04}.png".format(x))
        img = img_loader.load_image(img_path, True)
        imgs.append(img)
    return imgs

class Score(pygame.sprite.Sprite):
    """
    For counting and displaying of score.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font("data/freesansbold.ttf", 32)
        self.font.set_italic(1)
        self.color = Color('white')
        self._current = 0
        self.lastscore = -1
        self.best = -1
        self.update()
        self.rect = self.image.get_rect(bottomleft=screen_rect.bottomleft)

    def update(self):
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Score: {}".format(self.score)
            self.image = self.font.render(msg, True, self.color)
    
    @property
    def score(self):
        return self._current
    
    @score.setter
    def score(self, value):
        self._current = value
        if not self._current % YellowStar.period:
            YellowStar() # auto-added to group
            

class YellowStar(pygame.sprite.Sprite):
    """
    Power-up for Player.
    """
    image_size = (30, 30)
    speed = global_speed
    # see Score()
    period = 20
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midtop=screen_rect.midtop)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > screen_rect.bottom:
            self.kill()
            
    def activate(self, player):
        TempShield(player)
        self.kill()
        
    
class TempShield(pygame.sprite.Sprite):
    """
    Time-based shield.
    """
    duration = fps * 5
    images = []
    def __init__(self, actor):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = TempShield.duration
        self.actor = actor
        actor.shield = self

    def update(self):
        self.rect.center = self.actor.rect.center
        self.life = self.life - 1
        if self.life <= 0: 
            self.kill()
            self.actor.shield = None 


        

def exit_game():
    """
    Exit the game.            
    """
    save_settings(config, audio, score)
    # TODO: ask for confirmation
    raise SystemExit(0)
            
def load_sprite_images(loader):
    Player.images = loader.load_images("player_left.png", "player.png", 
                                       "player_right.png", 
                                       convert_alpha=True)
    Alien.images = [loader.load_image("enemy_ship.png", True)]
    Shot.images = [loader.load_image("laser_red.png")]
    Bomb.images = [loader.load_image("laser_green.png")]
    img = loader.load_image("star_yellow.png", True)
    img = pygame.transform.smoothscale(img, 
                                       YellowStar.image_size)
    YellowStar.images = [img]
    Explosion.images = load_expl_images(loader)
    BigExplosion.set_and_scale_images(Explosion.images)
    TempShield.images = [loader.load_image("shield.png", True)]
    img = loader.load_image("cruiser.png", True)
    img = pygame.transform.rotozoom(img, 90, 0.3)
    Cruiser.images = [img]
    
def create_groups():
    global aliens, shots, bombs, powerups, s_all, last_alien
    aliens = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    s_all = pygame.sprite.RenderUpdates()
    last_alien = pygame.sprite.GroupSingle()
    
def group_sprites():
    """
    Assign default groups to each sprite class.
    """
    Player.containers = s_all
    Alien.containers = aliens, s_all, last_alien
    Shot.containers = shots, s_all
    Bomb.containers = bombs, s_all
    YellowStar.containers = powerups, s_all
    Explosion.containers = s_all
    BigExplosion.containers = s_all
    Score.containers = s_all
    TempShield.containers = s_all
    Cruiser.containers = aliens, s_all
    
class EnemyGenerator():
    alien_reload = 40
    speed_up_period = 10
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.count = 0
    
    def next(self):
        """
        Generate next enemy.
        """
        self.count += 1
        if not self.count % self.speed_up_period:
            self.alien_reload -= 1
        if not self.count % Cruiser.entry_period:
            Cruiser() # auto-added to group
        else:
            Alien() # auto-added to group
            
    def update(self):
        if self.alien_reload:
            self.alien_reload -= 1
        else:
            self.next()
            self.alien_reload = EnemyGenerator.alien_reload

def main():
    """
    Init everything and show menu.
    """
    pygame.init()
    
    create_groups()
    group_sprites()
    
    if getattr(sys, 'frozen', False):
        # frozen
        dir_ = os.path.dirname(sys.executable)
    else:
        # not frozen
        dir_ = os.path.dirname(os.path.realpath(__file__))
        
    data_dir = os.path.join(dir_, "data")
    Audio.init(data_dir)
    
    global screen_rect
    screen_rect = Rect(0, 0, 640, 480)
    
    global audio, score
    audio = Audio()
    score = Score()
    load_settings(config, audio, score)
    
    TITLE = "Aliens From Space"
    pygame.display.set_caption(TITLE)
    
    global screen
    screen = pygame.display.set_mode(screen_rect.size)
    
    global bg_image
    loader = ImageLoader(data_dir)
    bg_image = loader.load_image("background.png")
    load_sprite_images(loader)
    
    global menu
    font = pygame.font.Font("data/freesansbold.ttf", 48)
    menu = GameMenu(screen, font, audio, bg_image, exit_game, data_dir)
    
    global enemy_generator
    enemy_generator = EnemyGenerator()
    
    while True:
        try:
            menu.show_menu(False, True)
        except ContinueException:
            screen.blit(bg_image, (0, 0), screen_rect)
            pygame.display.update()
            audio.play_bg()
            start_game()
    
    exit_game()

def start_game():
    # init game variables
    clock = pygame.time.Clock()
    global exiting
    exiting = None
    enemy_generator.reset()
    
    # init starting sprites
    for sprite in s_all:
        if not type(sprite) == Score:
            sprite.kill()
    player = Player()
    score._current = 0
    Alien() # auto-added to group
    
    def kill_player():
        """
        Kill Player (if appropriate).
        """
        if player.shield is None:
            BigExplosion(player)
            player.kill()
            global exiting
            exiting = Explosion.default_life
            pygame.mixer.music.fadeout(1000)
            
            
    while player.alive() or exiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == KEYDOWN: 
                if event.key == K_ESCAPE:
                    try:
                        menu.show_menu()
                    except ContinueException:
                        audio.play_bg()
                        screen.blit(bg_image, (0, 0))
                        pygame.display.update()
                
        # clear last drawn
        s_all.clear(screen, bg_image)
         
        # update everything
        s_all.update()

        # player input
        keystate = pygame.key.get_pressed()
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        if direction == 0:
            direction = keystate[K_d] - keystate[K_a]
        player.move(direction)
        firing = keystate[K_SPACE]
        if (not player.reloading and firing 
            and len(shots) < Player.max_shots):
            Shot(player.gunpos())
#             shoot_sound.play()
        player.reloading = firing
        
        # FIXME: for testing only
        if keystate[pygame.K_KP_PLUS]:
            score.score += 1
        elif keystate[pygame.K_KP_MINUS]:
            score.score -= 1
        
        # Create new alien
        enemy_generator.update()
            
        # drop bombs
        if (last_alien 
            and random.random() < Alien.bomb_odds):
            Bomb(last_alien.sprite)
        
        # detect collisions
        for alien in pygame.sprite.spritecollide(player, aliens, 1):
            Explosion(alien)
            score.score += 1
            kill_player()

        for alien in pygame.sprite.groupcollide(aliens, shots, 1, 1).keys():
            Explosion(alien)
            score.score += 1

        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            Explosion(bomb)
            kill_player()
            
        for powerup in pygame.sprite.spritecollide(player, powerups, False):
            powerup.activate(player)

        # draw screen
        dirty = s_all.draw(screen)
        pygame.display.update(dirty)
        
        if exiting:
            exiting -= 1
        
        # cap framerate
        clock.tick(fps)
    
    menu.show_score(score)
        
if __name__ == '__main__':
    main()