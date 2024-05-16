from settings import *
import pygame
from pytmx.util_pygame import load_pygame
from level import Level
from support import *
import pygame_widgets.button
import pygame_widgets.textbox

quit_button = pygame_widgets.button.Button(
        screen, 375, 291, 50, 20,
        text='Quit',
        fontSize=15, margin=0,
        inactiveColour=(255, 255, 255),
        pressedColour=(0, 255, 15),
        radius=0,
        onClick= lambda: pygame.quit()
    )

class Game:
    def __init__(self):

        pygame.init()

        # Initialisation de l'horloge interne
        self.clock = pygame.time.Clock()

        # Creation de l ecran de jeu
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

        # Set window title
        pygame.display.set_caption("Escape of the RedHood")

        self.assets()

        self.tmx_maps = {0: load_pygame("Fichier Tiled/NiveauTest2.tmx")}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)

        paused = False
        running = False
        pause_cooldown = 0

    def run(self):
        running = True
        timeF = self.clock.tick()/1000
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.current_stage.run(timeF)
            pygame.display.update()

    def assets(self):
        self.level_frames = {
            'player': import_sub_folders('sprites', 'RedHoodSprite')
        }

    def pause(self):
        while running :
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

        # Update player position
        pygame.event.pump()
        if not paused:
            game.run()
            quit_button.hide()
        else :
            quit_button.draw()
            quit_button.show()
            pygame_widgets.update(events)

    pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()