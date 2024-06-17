from settings import *
import pygame
from nonplayablecharacter import NonPlayableCharacter
from player import Player
from pygame.math import Vector2 as vector
from timer import Timer

class Ennemy(NonPlayableCharacter):
    def __init__(self, position, group, collision_sprites, frames, player: Player):
        super().__init__(position, group, collision_sprites, frames)

        self.state = "Death"
        self.speed = 5
        self.player = player

        self.attack_connecting = False

        self.timers = {
            'attack duration': Timer(400),
            'cooldownhit': Timer(200)
        }

    def input(self):
        input_vector = vector(0, 0)

        if not self.dead:
            player_center = self.player.rect.centerx
            ennemy_center = self.rect.centerx

            if max(player_center, ennemy_center) - min(player_center, ennemy_center) < 200:
                if player_center > ennemy_center:
                    self.state = "Run"
                    input_vector.x += 1
                    self.facing_right = True

                else:
                    self.facing_right = False
                    self.state = "Run"
                    input_vector.x -= 1
                    self.facing_right = False

                self.player_interaction()

            elif not self.facing_right:
                if not self.on_surface["left"]:
                    self.facing_right = False
                    self.state = "Run"
                    input_vector.x -= 1
                else:
                    self.facing_right = True
                    self.state = "Run"
                    input_vector.x += 1

            else:
                if not self.on_surface["right"]:
                    self.facing_right = True
                    self.state = "Run"
                    input_vector.x += 1
                else:
                    self.facing_right = False
                    self.state = "Run"
                    input_vector.x -= 1

        if self.attacking:
            input_vector.x = 0
        
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def player_interaction(self):

        player_center = self.player.rect.center
        ennemy_center = self.rect.center
        difference = (max(player_center[0], ennemy_center[0]) - min(player_center[0], ennemy_center[0]), max(player_center[1], ennemy_center[1]) - min(player_center[1], ennemy_center[1])) 

        if self.player.attacking and self.player.attack_position[0] >= self.rect.left and max(self.player.attack_position[1], self.rect.centery) - min(self.player.attack_position[1], self.rect.centery) <= 20 and (self.player.facing_right and self.player.attack_position[0] >= self.rect.left or not self.player.facing_right and self.player.attack_position[0] <= self.rect.right):
            self.dead = True
            self.frame_index = 0
            self.state = "Death"
            print("Collision with player detected : NPC died")

        elif not self.dead and difference[0] <= 20 and difference[1] <= 20:
            self.attack()
            self.attacking = True

            if not self.dead:
                if not self.timers['cooldownhit'].active and not self.attack_connecting:
                    self.timers['cooldownhit'].activate()

                print(self.attack_connecting)

                if difference[1] <= 20:
                    self.attack_connecting = True
        print('Timer', self.timers['cooldownhit'].active)
        if not self.timers['cooldownhit'].active and self.attack_connecting:
            self.player.dead = True
            print("Collision with player detected : Player died")

    def animate(self, GameTime):

        if self.dead and self.frame_index <= len(self.frames[self.state]) -1:
            self.frame_index += ANIMATION_SPEED * GameTime
            self.state = "Death"

        elif not self.dead:
            self.frame_index += ANIMATION_SPEED * GameTime
            if self.state == 'Attack' and self.frame_index >= len(self.frames[self.state]):
                self.state = 'Idle'
            if self.state == 'Jump' and self.frame_index == len(self.frames[self.state]):
                self.state = 'Fall'

            if self.attacking and self.frame_index > len(self.frames[self.state]):
                self.attacking = False

        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)


    def get_state(self):
        if not self.dead:
            if self.on_surface['floor']:
                if self.attacking:
                    self.state = 'Attack'
                else:
                    self.state = 'Idle' if self.direction.x == 0 else 'Run'
            else:
                self.state = 'Jump' if self.direction.y < 0 else 'Fall'