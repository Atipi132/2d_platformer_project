import pygame
import pygame.ftfont
import pygame_widgets.button
import pygame_widgets.textbox
from pytmx.util_pygame import load_pygame
from settings import *
from support import *
from level import Level
from os import environ

class Game:
    def __init__(self):

        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.font.init()

        # Initialization of the internal clock
        self.clock = pygame.time.Clock()

        self.paused = False
        self.running = True

        # Creation of the gaming screen :
        with open("settings.py", "r") as settings:
            size = tuple(settings.readlines()[0].split("= ")[1].split(", "))
            print(size)
            settings.close()
        self.size  = (int(size[0]), int(size[1]))
        self.display_surface = pygame.display.set_mode((self.size[0], self.size[1]))

        # Set window title :
        pygame.display.set_caption("Escape of the RedHood")

        self.assets()

        # Path to the map :
        self.tmx_maps = {0: load_pygame("TiledFiles/Level1.tmx"),
                         1: load_pygame("TiledFiles/Level2.tmx")}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)
        self.pause_cooldown = 0

        # Building the quit button of the game
        self.quit_button = pygame_widgets.button.Button(
            self.display_surface, self.size[0]/2 - 100, self.size[1]/2, 200, 80,
            text='Quit',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 0, 0),
            radius=0,
            onClick=lambda: self.setRunning(False)
        )

        # Building the resume button of the game
        self.resumeButton = pygame_widgets.button.Button(
            self.display_surface, self.size[0]/2 - 100, self.size[1]/2 - 120, 200, 80,
            text='Resume',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 0, 0),
            radius=0,
            onClick=lambda: self.setPaused(False)
        )

    def run(self):
        GameTime = self.clock.tick()/2000

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

            if not self.paused:
                self.current_stage.run(GameTime)
            else :
                pygame_widgets.update(events)
            
            if self.current_stage.player.dead:
                pygame_widgets.update(events)

            pygame.display.update()

        pygame.quit()

    # Path to the sprites of the character
    def assets(self):
        self.level_frames = {
            'player': import_sub_folders('sprites', 'RedHoodSprite'),
            'squelette': import_sub_folders('sprites', 'Skeleton'),
            'witch': import_sub_folders('sprites', 'witch')
        }

    def setRunning(self, setter: bool):
        self.running = setter

    def setPaused(self, setter: bool):
        self.paused = setter

    def setSize(self, setter: tuple):
        self.size = setter