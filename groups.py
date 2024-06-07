import pygame
from pygame.math import Vector2 as vector
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_position, timeF):
        self.offset.x = -(target_position[0] - WIDTH/2)
        self.offset.y = -(target_position[1] - HEIGHT / 2)
        for sprite in self:
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def kill(self):
        for sprite in self.sprites():
            sprite.kill()