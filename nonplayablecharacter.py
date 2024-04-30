from player import Player
import pygame
import time

class NonPlayableCharacter(Player):
    def __init__(self, startx: int, starty: int, collision_group, player: Player):
        super().__init__(startx, starty, collision_group)
        self.side = 'L'
        group = pygame.sprite.Group()
        group.add(player)
        self.player_group = group

        # Relatif à l'attaque
        self.attack_images = [
            pygame.image.load("sprites/Squelette/Attaque/Squelette-Attaque ({}).png".format(i))
            for i in range(1, 18)]
        self.attack_index = 0
        self.currently_attacking = False
        self.attack_finished = True
        self.attack_cooldown = 0

        # Relatif à la course
        self.walk_cycle = [pygame.image.load("sprites/Squelette/Marche/Squelette-Marche ({}).png".format(i)) for i in
                           range(1, 13)]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 1

        #Relatif à la mort
        self.death_images = [pygame.image.load("sprites/Squelette/Mort/Squelette-Mort ({}).png".format(i)) for i in
                           range(1, 40)]
        self.death_index = 0
        self.death = False

    def update(self):
        horizontal_speed = 0
        onground = self.check_collisions(0, 1, self.collision_group)

        if not self.death :
            if self.side == 'L':
                if not self.check_collisions(-1, 0, self.collision_group):
                    self.facing_left = True
                    self.walk_animation()
                    horizontal_speed = -self.speed
                else:
                    self.facing_left = False
                    self.walk_animation()
                    horizontal_speed = self.speed
                    self.side = 'R'
        
            else:
                if not self.check_collisions(1, 0, self.collision_group):
                    self.facing_left = False
                    self.walk_animation()
                    horizontal_speed = self.speed
                else:
                    self.facing_left = False
                    self.walk_animation()
                    horizontal_speed = self.speed
                    self.side = 'L'
        else :
            self.death_animation()

        if not onground:
            self.verticalspeed += self.gravity

        self.move(horizontal_speed, self.verticalspeed)
        if self.check_collisions(0, 0, self.player_group):
            if self.player_group.sprites()[0].currently_attacking == True and self.facing_left != self.player_group.sprites()[0].facing_left:
                print("Collision with player detected : NPC died")
                self.death = True

            elif not self.death :
                self.player_group.sprites()[0].dead = True
                print("Collision with player detected : Player died")

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0
    def attack_animation(self):
        if not self.attack_finished:
            self.image = self.attack_images[self.attack_index]
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
            self.attack_index += 1

            if self.attack_index >= len(self.attack_images):
                self.attack_index = len(self.attack_images) - 1
                self.attack_finished = True
        if self.attack_finished == True :
            self.attack_index = 0

    def death_animation(self):
        self.image = self.death_images[self.death_index]
        if self.death_index < len(self.death_images)-1 :
            self.death_index += 1
        if self.death_index == len(self.death_images)-1 :
            self.kill()
