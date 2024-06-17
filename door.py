import pygame
from pytmx.util_pygame import load_pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], group: pygame.sprite.Group, collision_sprites: pygame.sprite.Group, level):
        super().__init__(group)

        self.image = pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png")

        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()

        self.collision_sprites = collision_sprites

        self.tmx_maps = {0: load_pygame("TiledFiles/Level1.tmx"),
                         1: load_pygame("TiledFiles/Level2.tmx")}
        self.level = level

    def collision(self): # Collision with the door
        for sprite in self.collision_sprites:
            if self.rect.left == sprite.rect.right:
                print("door collision detected")
                self.level.ReloadLevel = True
                self.level.ReloadTheLevel(self.tmx_maps[1], self.level.level_frames)
                self.level.tmx_map = self.tmx_maps[1]
                self.tmx_maps.pop(0)

    def update(self, GameTime):
        self.old_rect = self.rect.copy()
        self.collision()
