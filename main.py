import pygame
from map import Map
from player import Player
from ennemy import Ennemy
def main():
    # Screen dimensions
    WIDTH, HEIGHT = 800, 602

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set window title
    pygame.display.set_caption("DKC Remaster")

    # Set background
    background = pygame.image.load("background/bg.png")

    # Set map
    map = Map("""
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XXXXXXXXXXXXXXXXXX
              XoooooXXXXXXXXXXXX
              oooooooooooooooooo
              XXXXoooXXXXXXXXXXX
              """).load()
    
    player = Player(WIDTH // 2, HEIGHT // 2, map)

    npc_sprite_group = pygame.sprite.Group()
    
    npc = Ennemy(WIDTH // 2 - 200, HEIGHT // 2 + 100, map, player)
    npc_sprite_group.add(npc)

    pygame.init()

    # Setup clock
    clock = pygame.time.Clock()

    running = True
    while running and not player.dead:
        # Check for game quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player position
        pygame.event.pump()
        player.update()
        npc.update()

        # Draw background
        for y in range(0, 600, 512):
                for x in range(0, 800, 512):
                    screen.blit(background, (x,y))
                    
        # Draw screen
        player.draw(screen)
        npc_sprite_group.draw(screen)
        map.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()