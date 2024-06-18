import pygame
from pytmx.util_pygame import load_pygame

class End(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], group: pygame.sprite.Group, collision_sprites: pygame.sprite.Group, level):
        super().__init__(group) # Initialize the parent class (Sprite)
        # Load the image for the door sprite
        self.image = pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png")
        # Set the position of the door sprite
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()
        # Group of sprites to check collisions
        self.collision_sprites = collision_sprites
        # Dictionary of Tiled maps
        self.tmx_maps = {0: load_pygame("TiledFiles/End.tmx")}
        self.level = level

    def collision(self): # Collision with the door
        for sprite in self.collision_sprites:
            if self.rect.left == sprite.rect.right: # Check for collision on the left side
                print("End")
                self.level.ReloadLevel = True # Set the level reload flag to True
                self.level.ReloadTheLevel(self.tmx_maps[0], self.level.level_frames)
                self.level.tmx_map = self.tmx_maps[0] # Update the current map to the next map
                self.tmx_maps.pop(0)

    def update(self, GameTime):
        self.old_rect = self.rect.copy() # Update the old rectangle to the current position
        self.collision() # Check for collisions and handle them
