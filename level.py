import pygame
from sprite import Sprite
from player import Player
from ennemy import Ennemy
from groups import AllSprites
from pytmx import TiledMap
from door import Door
from settings import *
import pygame_widgets.button
import pygame_widgets.textbox
from witch import Witch

class Level:
    def __init__(self, tmx_map: TiledMap, level_frames: dict):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.tmx_map = tmx_map
        self.level_frames = level_frames

        self.setup(tmx_map, level_frames)
        self.ReloadLevel = False

        self.retryButton = pygame_widgets.button.Button(
            self.display_surface, WIDTH / 2 - 100, HEIGHT / 2 - 120, 200, 80,
            text='Retry the level',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 0, 0),
            radius=0,
            onClick=lambda: self.ClickRetryButton()
        )

    def setup(self, tmx_map, level_frames: dict):
        for x,y, surface in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == "Player":
                self.player = Player(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['player']
                )
            if obj.name == "Skeleton":
                Ennemy(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['squelette'],
                    player=self.player
                )

            if obj.name == "Witch":
                Witch(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['witch'],
                    player=self.player
                )
            if obj.name == "door":
                Door(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=pygame.sprite.Group(self.player),
                    level=self
                )


    def gameover(self, player):
        events = pygame.event.get()
        if player.dead:
            self.retryButton.draw()
            self.retryButton.show()
            pygame_widgets.update(events)
        else:
            self.retryButton.hide()

    def ClickRetryButton(self): # Relié au bouton retry, le but est de savoir si le bouton est cliqué pour recommencer le niveau avec RetryTheLevel
        self.ReloadLevel = True

    def ReloadTheLevel(self, tmx_map, level_frames): # Recommence le niveau, supprimes le niveau puis le reconstruit
        if self.ReloadLevel:
            self.all_sprites.kill()
            self.setup(tmx_map, level_frames)
            self.ReloadLevel = False

    def run(self, GameTime):
        self.all_sprites.update(GameTime)
        self.display_surface.fill('gray')
        self.all_sprites.draw(self.player.rect.center, GameTime)
        self.gameover(self.player)
        self.ReloadTheLevel(self.tmx_map, self.level_frames)
