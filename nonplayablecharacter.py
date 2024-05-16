from player import Player
import pygame

class NonPlayableCharacter(Player):
    def __init__(self, startx: int, starty: int, collision_group, player: Player):
        super().__init__(startx, starty, collision_group)
        group = pygame.sprite.Group()
        group.add(player)
        
        self.side = 'L'
        self.player = player
        self.player_group = group

        # Relatif à l'attaque
        self.attack_images = [
            pygame.image.load("sprites/Squelette/Attaque/Squelette-Attaque ({}).png".format(i))
            for i in range(1, 19)]
        self.attack_index = 0
        self.currently_attacking = False
        self.attack_finished = True
        self.attack_cooldown = 0

        # Relatif à la course
        self.walk_cycle = [pygame.image.load("sprites/Squelette/Marche/Squelette-Marche ({}).png".format(i)) for i in
                           range(1, 14)]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 1

        #Relatif à la mort
        self.death_images = [pygame.image.load("sprites/Squelette/Mort/Squelette-Mort ({}).png".format(i)) for i in
                           range(1, 41)]
        self.death_index = 0
        self.death = False

    def update(self):
        horizontal_speed = 0
        onground = self.check_collisions(0, 1, self.collision_group) # Permet de définir lorsque le personnage est au sol

        if not self.death : # Adopte le comportement classique lorsqu'il est vivant
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

            self.move(horizontal_speed, self.verticalspeed)
            if self.check_collisions(0, 0, self.player_group):
                self.player_interaction()

        else :
            self.death_animation()

        if not onground:
            self.verticalspeed += self.gravity

    def player_interaction(self):
        pass


    def walk_animation(self): #Gestion de l'animation de marche
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0
            
    def attack_animation(self): #Gestion de l'animation d'attaque
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

    def death_animation(self): #Gestion de l'animation de mort
        self.image = self.death_images[self.death_index]
        if self.death_index < len(self.death_images)-1 :
            self.death_index += 1
        if self.death_index == len(self.death_images)-1 :
            self.kill()
