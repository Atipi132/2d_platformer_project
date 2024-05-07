import pygame
import pygame_widgets.button
import pygame_widgets.textbox
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
    
    pygame.font.init()
    pygame.init()
    
    quit_button = pygame_widgets.button.Button(
        screen, 375, 291, 50, 20, 
        text='Quit',
        fontSize=15, margin=0,
        inactiveColour=(255, 255, 255),
        pressedColour=(0, 255, 15), 
        radius=0,
        onClick= lambda: pygame.quit()
    )

    # Setup clock
    clock = pygame.time.Clock()

    paused = False
    running = True
    pause_cooldown = 0
    while running and not player.dead:
        clock.tick(60)

        # Check for game quit event
        key = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        if pause_cooldown > 0:
            pause_cooldown -= 1
        elif key[pygame.K_ESCAPE]:
            paused = not paused
            pause_cooldown = 15


        # Draw background
        for y in range(0, 600, 512):
                for x in range(0, 800, 512):
                    screen.blit(background, (x,y))
                    
        # Update player position
        pygame.event.pump()
        if not paused:
            player.update()
            npc.update()
            quit_button.hide()
        else : 
            quit_button.draw()
            quit_button.show()
            pygame_widgets.update(events)

        # Draw screen
        player.draw(screen)
        npc_sprite_group.draw(screen)
        map.draw(screen)
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()