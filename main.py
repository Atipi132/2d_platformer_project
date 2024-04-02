import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_src: str, startx: int, starty: int):
        super().__init__()

        self.image = pygame.image.load(image_src)
        self.rect = self.image.get_rect()
        self.rect.center = (startx, starty)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("sprites/dk_sprite.png", startx, starty)

        self.speed = 4

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.move(0, -5)
        if key[pygame.K_DOWN]:
            self.move(0, 5)
        if key[pygame.K_LEFT]:
            self.move(-self.speed, 0)
        if key[pygame.K_RIGHT]:
            self.move(self.speed, 0)

    def move(self, x: int, y: int):
        self.rect.move_ip([x,y])

class Box(Sprite):
    def __init__(self, startx: int, starty: int, image_src: str):
        super().__init__(image_src, startx, starty)


def main():
    # Screen dimensions
    WIDTH, HEIGHT = 800, 600

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set window title
    pygame.display.set_caption("DKC Remaster")

    # Set background
    background = pygame.image.load("background/bg.png")

    # Set player and objects
    player = Player(WIDTH // 2, HEIGHT // 2)
    oil_Drum = Box(100, 100, "sprites/Oil_Drum.png")

    pygame.init()

    # Setup clock
    clock = pygame.time.Clock()

    running = True
    while running:
        # Check for game quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player position
        pygame.event.pump()
        player.update()

        # Draw background
        for y in range(0, 600, 512):
                for x in range(0, 800, 512):
                    screen.blit(background, (x,y))
        # Draw screen
        player.draw(screen)
        oil_Drum.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()