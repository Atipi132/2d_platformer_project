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
    def __init__(self, startx, starty, collisionGroup):
        super().__init__("sprites/idle.gif", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("sprites/jump.png")

        self.walk_cycle = [pygame.image.load("sprites/JungleRun/Course- ({}).png".format(i)) for i in range(1, 8)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 20
        self.min_jumpspeed = 3
        self.previous_key = pygame.key.get_pressed()
        self.verticalspeed = 0
        self.gravity = 1
        self.collisionGroup = collisionGroup

    def update(self):

        horziontalspeed = 0
        onground = self.check_collisions(0, 1)


        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            horziontalspeed = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            horziontalspeed = self.speed
        else:
            self.image = self.stand_image    

        if key[pygame.K_UP] and onground:
            self.verticalspeed = -self.jumpspeed

        # variable height jumping
        if self.previous_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.verticalspeed < -self.min_jumpspeed:
                self.verticalspeed = -self.min_jumpspeed
        self.previous_key = key


        if self.verticalspeed < 10 and not onground:
            self.jump_animation()
            self.verticalspeed += self.gravity


        if self.verticalspeed > 0 and onground:
            self.verticalspeed = 0


        self.move(horziontalspeed, self.verticalspeed)


    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, x: int, y: int):
        dx = x
        dy = y
        
        while self.check_collisions(0, dy):
            dy -= 1 if dy > 0 else -1 if dy <0 else 0

        while self.check_collisions(dx, dy):
            dx -= 1 if dx > 0 else -1 if dx < 0 else 0

        self.rect.move_ip([dx, dy])

    def check_collisions(self, x: int, y: int):
        self.rect.move_ip([x,y]) # move the player
        collide = pygame.sprite.spritecollideany(self, self.collisionGroup) # check for collision
        self.rect.move_ip([-x,-y]) # move the player back to the original coordinates ; all of this is done before the player is drawn to the screen so the user doesn't see anything
        return collide

    

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
    boxes = pygame.sprite.Group()
    for bx in range(0,600,32):
        boxes.add(Box(bx, 450, "sprites/Oil_Drum.png"))

    big_box = Box(64, 400, "sprites/Oil_Drum.png")
    boxes.add(big_box)

    player = Player(WIDTH // 2, HEIGHT // 2, boxes)

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
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()