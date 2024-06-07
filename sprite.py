import pygame
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, group):
        super().__init__(group)

        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()

class AnimatedSprite(Sprite):
    def __init__(self, position, frames, groups, animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(position, self.frames[self.frame_index], groups)
        self.animation_speed = animation_speed

    def animate(self, timeF):
        self.frame_index += self.animation_speed * timeF
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, time):
        self.animate(time)