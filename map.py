import pygame
from box import Box

class Map():
    def __init__(self, map_string: str):
        self.map_string = map_string

    def load(self):
        map = pygame.sprite.Group()

        max_sprite_height = 32
        i = 0
        j = 0

        for line in self.map_string.splitlines():
            for char in line:
                match char:
                    case "o":
                        map.add(Box(i, j, "sprites/Oil_Drum.png"))
                        i += 32
                        max_sprite_height = max(max_sprite_height, 46)
                    case "X":
                        i += 32
            j += max_sprite_height
            max_sprite_height = 32
            i = 0

        return map