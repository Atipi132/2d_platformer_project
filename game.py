from settings import *
import pygame
from pytmx.util_pygame import load_pygame
from level import Level
from support import *
import pygame_widgets.button
import pygame_widgets.textbox

class Game:
    def __init__(self):

        pygame.init()

        # Initialisation de l'horloge interne
        self.clock = pygame.time.Clock()

        self.paused = False
        self.running = True

        # Creation de l ecran de jeu
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

        # Set window title
        pygame.display.set_caption("Escape of the RedHood")

        self.assets()

        self.tmx_maps = {0: load_pygame("Fichier Tiled/Level1.tmx")}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)       
        self.pause_cooldown = 0

        self.quit_button = pygame_widgets.button.Button(
            self.display_surface, WIDTH/2, HEIGHT/2, 50, 20,
            text='Quit',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 255, 15),
            radius=0,
            onClick= lambda: self.setRunning(False)
        )

        self.resume_button = pygame_widgets.button.Button(
            self.display_surface, WIDTH/2, HEIGHT/2 - 40, 50, 20,
            text='Resume',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 255, 15),
            radius=0,
            onClick= lambda: self.setPaused(False)
        )

    def run(self):
        timeF = self.clock.tick()/2000

        pygame.mixer.music.load('sounds\\music\\main_music.mp3')
        pygame.mixer.music.play(-1)

        while self.running:
            self.pause_cooldown -= 1 if self.pause_cooldown != 0 else 0
            key = pygame.key.get_pressed()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.setRunning(False)
            if key[pygame.K_ESCAPE] and self.pause_cooldown == 0:
                self.setPaused(not self.paused)
                self.pause_cooldown = 500 if self.paused else 50
            elif key[pygame.K_e]:
                window_size = pygame.display.get_window_size()
                window_size = [window_size[0] +10, window_size[1] + 10]
                self.display_surface = pygame.display.set_mode(window_size)

            if not self.paused:
                self.current_stage.run(timeF)
                self.quit_button.hide()
            else :
                self.quit_button.draw()
                self.quit_button.show()
                pygame_widgets.update(events)

            pygame.display.update()

        pygame.quit()

    def assets(self):
        self.level_frames = {
            'player': import_sub_folders('sprites', 'RedHoodSprite'),
            'squelette': import_sub_folders('sprites', 'Squelette')
        }

    def setRunning(self, setter: bool):
        self.running = setter

    def setPaused(self, setter: bool):
        self.paused = setter