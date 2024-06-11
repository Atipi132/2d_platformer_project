import pygame
from pygame.math import Vector2 as vector
import math
import random
from player import Player
from nonplayablecharacter import NonPlayableCharacter
from timer import Timer



class Witch(NonPlayableCharacter):
    def __init__(self, position, group, collision_sprites, frames, player: Player):
        super().__init__(position, group, collision_sprites, frames)

        self.state = "Idle"
        self.speed = 5
        self.player = player
        self.gravity = 0
        self.charging = False
        self.teleporting = False

        self.timers = {
            'charge duration': Timer(1200), # Temps de charge de l'attaque magique
            'attack duration': Timer(400), # Temps d'une attaque magique
            'cooldown': Timer(900) # Temps avant de pouvoir de nouveau agir
        }

    def input(self):
        input_vector = vector(0, 0)

        if not self.dead:
            player_center = self.player.rect.centerx
            witch_center = self.rect.centerx

            if max(player_center, witch_center) - min(player_center, witch_center) < 200:
                if player_center > witch_center:
                    self.facing_right = True


                else:
                    self.facing_right = False

                self.player_interaction()

            elif not self.facing_right:
                if not self.on_surface["left"]:
                    self.facing_right = False
                else:
                    self.facing_right = True

            else:
                if not self.on_surface["right"]:
                    self.facing_right = True
                else:
                    self.facing_right = False

    def player_interaction(self):
        player_center = self.player.rect.center
        witch_center = self.rect.center

        difference = (max(player_center[0], witch_center[0]) - min(player_center[0], witch_center[0]),
                      max(player_center[1], witch_center[1]) - min(player_center[1], witch_center[1]))

        if not self.attacking:

            if self.player.attacking and self.facing_right != self.player.facing_right and self.player.attack_position[
                0] >= self.rect.left and max(self.player.attack_position[1], self.rect.centery) - min(
                    self.player.attack_position[1], self.rect.centery) <= 20:
                self.dead = True
                self.frame_index = 0
                self.state = 'Death'
                print("Collision with player detected : NPC died")

            if not self.charging and not self.timers['cooldown'].active:

                if difference[1] <= 40 :
                    self.frame_index = 0
                    self.teleporting = True
                    self.rect.centerx += random.randint(-200, 200)
                    #self.rect.centery += random.randint(-200, 200)

                if not self.dead:
                    self.charging = True
                    self.timers['charge duration'].activate()

    def animate(self, timeF):
        if not self.dead:
            self.frame_index += 1 * timeF
            if self.timers['charge duration'].active:
                self.state = 'Charge'

            if not self.timers['charge duration'].active and self.charging:
                if not self.timers['attack duration'].active:
                    self.attacking = True
                    self.charging = False
                    self.timers['attack duration'].activate()

            if self.attacking:
                if not self.facing_right:
                    self.state = 'Attaque'
                else:
                    self.state = 'Attaque'

            if self.attacking and not self.timers['attack duration'].active:
                self.attacking = False
                self.timers['cooldown'].activate()

            if self.teleporting and not self.frame_index == len(self.frames[self.state]):
                self.state = 'Teleportation'

            if self.state == 'Teleportation' and self.frame_index >= len(self.frames[self.state]):
                self.teleporting = False
                self.state = 'Idle'

            self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

        if self.dead:
            if not math.ceil(self.frame_index) == len(self.frames['Death']):
                self.frame_index += 1*timeF
                self.state = 'Death'

            self.image = self.frames['Death'][int(self.frame_index % len(self.frames['Death']))]

        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
