import pygame
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector

class Door(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], group : pygame.sprite.Group, collision_sprites : pygame.sprite.Group, level):
        super().__init__(group)

        self.image = pygame.image.load("C:\\Users\\hugop\\Documents\\ESIREM\\2A\\python\\2d_platformer_project\\sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png")

        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()

        self.collision_sprites = collision_sprites

        self.tmx_maps = {0: load_pygame("Fichier Tiled/Level1.tmx"),
                         1: load_pygame("Fichier Tiled/NiveauTest4.tmx")}
        self.level = level

    def collision(self):
        for sprite in self.collision_sprites:
            if self.rect.left == sprite.rect.right:
                print("door collision detected")
                self.level.retryLevel = True
                self.level.RetryTheLevel(self.tmx_maps[1], self.level.level_frames)
                self.level.tmx_map = self.tmx_maps[1]
                self.tmx_maps.pop(0)
        
    def update(self, timeF):
        self.old_rect = self.rect.copy()
        self.collision()