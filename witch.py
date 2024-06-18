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

        self.startingPositionX = self.rect.centerx
        self.startingPositionY = self.rect.centery
        self.maximumX = self.startingPositionX + 400
        self.minimumX = self.startingPositionX - 400
        self.maximumY = self.startingPositionY + 200
        self.minimumY = self.startingPositionY

        self.newPositionX = 0
        self.newPositionY = 0

        self.state = "Idle"
        self.speed = 5
        self.player = player
        self.gravity = 0
        self.charging = False
        self.teleporting = False
        self.TeleportationToAttack = False
        self.attack_connecting = False

        # Timers for various actions
        self.timers = {
            'teleportation cooldown' : Timer(120), #Teleportation Cooldown
            'charge duration': Timer(1200), # Charging time
            'attack duration': Timer(400), # Attacking time
            'cooldown': Timer(900), # Cooldown before action
            'cooldownhit': Timer(20) # Cooldown to make a hit less strong
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
        if not self.dead:
            if not self.attacking:

                if self.player.attacking and self.facing_right != self.player.facing_right and self.player.attack_position[
                    0] >= self.rect.left and max(self.player.attack_position[1], self.rect.centery) - min(
                        self.player.attack_position[1], self.rect.centery) <= 15:
                    self.dead = True
                    self.frame_index = 0
                    self.state = 'Death'
                    print("Collision with player detected : NPC died")

                if not self.charging and not self.timers['cooldown'].active:

                    if difference[0] <= 40:
                        self.teleportation()

                    if 40 <= difference[0] <= 100 and self.minimumY <= self.player.rect.centery <= self.maximumY and not self.timers['teleportation cooldown'].active:
                        if not self.TeleportationToAttack:
                            self.frame_index = 0
                        self.TeleportationToAttack = True
                        self.teleporting = True
                        self.timers['teleportation cooldown'].activate()
                        self.rect.centery = self.player.rect.centery + 10

            else:
                if not self.timers['cooldownhit'].active:
                    self.timers['cooldownhit'].activate()

                if difference[0] <= 90 and difference[1] <= self.rect.centery - self.rect.y:
                    self.attack_connecting = True

        if not self.timers['cooldownhit'].active and self.attack_connecting:
            self.player.dead = True
            print("Collision with player detected : Player died")

    def teleportation(self):
        self.frame_index = 0
        self.teleporting = True
        self.newPositionX = random.randint(-200, 200)
        self.newPositionY = random.randint(-100, 100)

        if self.rect.centerx + self.newPositionX < self.minimumX or self.rect.centerx + self.newPositionX > self.maximumX or self.rect.centery + self.newPositionY < self.minimumY or self.rect.centery + self.newPositionY > self.maximumY:
            self.teleportation()
        else:
            self.rect.centerx += self.newPositionX
            self.rect.centery += self.newPositionY

    def animate(self, GameTime):
        if not self.dead:
            self.frame_index += 1 * GameTime
            if self.timers['charge duration'].active:
                self.state = 'Charge'

            if not self.timers['charge duration'].active and self.charging:
                if not self.timers['attack duration'].active:
                    self.attacking = True
                    self.charging = False
                    self.timers['attack duration'].activate()

            if self.attacking:
                if not self.facing_right:
                    self.state = 'Attack'
                else:
                    self.state = 'Attack'

            if self.attacking and not self.timers['attack duration'].active:
                self.attacking = False
                self.timers['cooldown'].activate()

            if self.teleporting and not self.frame_index == len(self.frames[self.state]):
                self.state = 'Teleportation'

            if self.state == 'Teleportation' and self.frame_index >= len(self.frames[self.state]):
                self.teleporting = False

                if self.TeleportationToAttack:
                    self.charging = True
                    self.timers['charge duration'].activate()
                    self.TeleportationToAttack = False
                else:
                    self.state = 'Idle'

            self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

        if self.dead:
            if not math.ceil(self.frame_index) == len(self.frames['Death']):
                self.frame_index += 1 * GameTime
                self.state = 'Death'
                self.gravity += 1
                self.direction.y = self.gravity

            self.image = self.frames['Death'][int(self.frame_index % len(self.frames['Death']))]

        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
