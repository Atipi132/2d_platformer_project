import pygame
from box import Box

class Map():
    def __init__(self, map_string: str):
        self.map_string = map_string

    def load(self):
        oil_drum_image = pygame.image.load("sprites/Oil_Drum.png")
        map = pygame.sprite.Group()

        max_sprite_height = 32
        i = 0
        j = 0

        for line in self.map_string.splitlines():
            for char in line:
                match char:
                    case "o":
                        map.add(Box(oil_drum_image, i, j))
                        i += 32
                        max_sprite_height = max(max_sprite_height, 46)
                        print("oil barrel loaded")
                    case "X":
                        i += 32
                        print("void loaded")
            j += max_sprite_height
            max_sprite_height = 32
            i = 0

        return map