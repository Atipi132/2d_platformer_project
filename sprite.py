import pygame
from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, group):
        super().__init__(group)

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()

