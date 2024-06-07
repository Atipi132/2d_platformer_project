import pygame
from sprite import Sprite
from player import Player
from ennemy import Ennemy
from groups import AllSprites
from pytmx import TiledMap
from settings import *
import pygame_widgets.button
import pygame_widgets.textbox

class Level:
    def __init__(self, tmx_map: TiledMap, level_frames: dict):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.tmx_map = tmx_map
        self.level_frames = level_frames

        self.setup(tmx_map, level_frames)
        self.retryLevel = False

        self.quit_button = pygame_widgets.button.Button(
            self.display_surface, WIDTH / 2 - 100, HEIGHT / 2, 200, 80,
            text='Quit',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 255, 15),
            radius=0,
            onClick=lambda: self.setRunning(False)
        )

        self.retryButton = pygame_widgets.button.Button(
            self.display_surface, WIDTH / 2 - 100, HEIGHT / 2 - 120, 200, 80,
            text='Retry the level',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 255, 15),
            radius=0,
            onClick=lambda: self.ClickRetryButton()
        )



    def setup(self, tmx_map, level_frames: dict):
        for x,y, surface in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE , y * TILE_SIZE ), surface, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == "Player":
                self.player = Player(
                    position = (obj.x, obj.y),
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    frames = level_frames['player']
                )
            if obj.name == "Squelette":
                Ennemy(
                    position = (obj.x, obj.y),
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    frames = level_frames['squelette'],
                    player = self.player
                )

    def gameover(self, player):
        events = pygame.event.get()
        if player.dead:
            self.quit_button.draw()
            self.quit_button.show()
            self.retryButton.draw()
            self.retryButton.show()
            pygame_widgets.update(events)
        else:
            self.quit_button.hide()
            self.retryButton.hide()

    def ClickRetryButton(self): # Relié au bouton retry, le but est de savoir si le bouton est cliqué pour recommencer le niveau avec RetryTheLevel
        self.retryLevel = True

    def RetryTheLevel(self,timeF, tmx_map, level_frames): # Recommence le niveau, supprimes le niveau puis le reconstruit
        if self.retryLevel:
            self.all_sprites.kill()
            self.setup(tmx_map, level_frames)
            self.retryLevel = False


    def run(self, timeF):
        self.all_sprites.update(timeF)
        self.display_surface.fill('green')
        self.all_sprites.draw(self.player.rect.center, timeF)
        self.gameover(self.player)
        self.RetryTheLevel(self, self.tmx_map, self.level_frames)
