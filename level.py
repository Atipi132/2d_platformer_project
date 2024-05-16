import pygame
from sprite import Sprite
from player import Player
from ennemy import Ennemy
from groups import AllSprites
from settings import *

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        for x,y, surface in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE , y * TILE_SIZE ), surface, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'Player':
                self.player = Player(
                    position = (obj.x, obj.y),
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    frames = level_frames['player']
                )
            # if obj.name == "Squelette":
            #     self.ennemy = Ennemy(
            #         position = (obj.x, obj.y),
            #         group = self.all_sprites,
            #         collision_sprites = self.collision_sprites,
            #         frames = level_frames['squelette'],
            #         player = self.player
            #     )

    def run(self, timeF):
        self.all_sprites.update(timeF)
        self.display_surface.fill('green')
        self.all_sprites.draw(self.player.rect.center, timeF)
