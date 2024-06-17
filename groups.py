import pygame
from pygame.math import Vector2 as vector

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, target_position, GameTime):
        with open("settings.py", "r") as settings:
            size = settings.readlines()[0].split("= ")[1].split(", ")
            settings.close()
        self.offset.x = -(target_position[0] - int(size[0])/2)
        self.offset.y = -(target_position[1] - int(size[1])/2)
        for sprite in self:
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def kill(self):
        for sprite in self.sprites():
            sprite.kill()