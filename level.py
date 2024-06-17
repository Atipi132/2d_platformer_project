import pygame
from sprite import Sprite
from player import Player
from ennemy import Ennemy
from groups import AllSprites
from pytmx import TiledMap
from door import Door
from settings import *
import pygame_widgets.button
import pygame_widgets.textbox
from witch import Witch

class Level:
    def __init__(self, tmx_map: TiledMap, level_frames: dict):
        self.display_surface = pygame.display.get_surface() # Get the main display surface

        self.all_sprites = AllSprites() # Group to contain all sprites
        self.collision_sprites = pygame.sprite.Group() # Group for collision detection


        self.tmx_map = tmx_map # Store the Tiled map
        self.level_frames = level_frames # Store frames for different entities

        self.setup(tmx_map, level_frames)  # Set up the level with map and frames
        self.ReloadLevel = False # Flag to indicate if the level needs to be reloaded

        # Initialize the retry button with its properties and click action
        self.retryButton = pygame_widgets.button.Button(
            self.display_surface, WIDTH / 2 - 100, HEIGHT / 2 - 120, 200, 80,
            text='Retry the level',
            fontSize=15, margin=0,
            inactiveColour=(255, 255, 255),
            pressedColour=(0, 0, 0),
            radius=0,
            onClick=lambda: self.ClickRetryButton()
        )

    def setup(self, tmx_map, level_frames: dict):
        for x,y, surface in tmx_map.get_layer_by_name('Terrain').tiles(): # Set up terrain tiles
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'): # Set up objects like player, enemies, and door
            if obj.name == "Player":
                self.player = Player(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['player']
                )
            if obj.name == "Skeleton":
                Ennemy(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['squelette'],
                    player=self.player
                )

            if obj.name == "Witch":
                Witch(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['witch'],
                    player=self.player
                )
            if obj.name == "door":
                Door(
                    position=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=pygame.sprite.Group(self.player),
                    level=self
                )


    def gameover(self, player): # Show the retry button when the player die
        events = pygame.event.get()
        if player.dead:
            self.retryButton.draw()
            self.retryButton.show()
            pygame_widgets.update(events)
        else:
            self.retryButton.hide()

    def ClickRetryButton(self): # Linked with the Retry button, it is needed because of the properties of the onClick componant of the button
        self.ReloadLevel = True

    def ReloadTheLevel(self, tmx_map, level_frames): # used to reload the level, it will delete all the loaded sprite before resetting new ones.
        if self.ReloadLevel:
            self.all_sprites.kill()
            self.setup(tmx_map, level_frames)
            self.ReloadLevel = False

    def run(self, GameTime): # Main game loop logic
        self.all_sprites.update(GameTime)  # Update all sprites
        self.display_surface.fill('gray')  # Clear the display surface
        self.all_sprites.draw(self.player.rect.center, GameTime)  # Draw all sprites centered on the player
        self.gameover(self.player)  # Check if the game is over
        self.ReloadTheLevel(self.tmx_map, self.level_frames)  # Reload the level if needed