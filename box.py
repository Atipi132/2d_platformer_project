import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, startx: int, starty: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (startx, starty)

    def draw(self, screen):
        screen.blit(self.image, self.rect)