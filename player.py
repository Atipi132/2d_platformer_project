from sprite import Sprite
import pygame
from attackbox import AttackBox

class Player(Sprite):
    def __init__(self, startx, starty, collision_group):
        super().__init__("sprites/RedHoodSprite/Course/RedHood-Idle.png", startx, starty)
        self.stand_image = self.image

        #Relatif au saut
        self.jump_images = [pygame.image.load("sprites/RedHoodSprite/Saut/RedHood-Saut ({}).png".format(i)) for i in
                            range(1, 56)]
        self.jump_index = 0
        self.jumping = False
        self.jump_finished = True

        self.jumpspeed = 20
        self.min_jumpspeed = 3

        #Relatif à l'attaque
        self.attack_images = [pygame.image.load("sprites/RedHoodSprite/Attaque/Attaque Faible/RedHood-AttaqueFaible ({}).png".format(i)) for i in range(1, 24)]
        self.attack_index = 0
        self.currently_attacking = False
        self.attack_finished = True
        self.attack_cooldown = 0

        #Relatif à la course
        self.walk_cycle = [pygame.image.load("sprites/RedHoodSprite/Course/RedHood-Course ({}).png".format(i)) for i in range(1, 49)]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 5

        self.dead = False
        self.previous_key = pygame.key.get_pressed()
        self.verticalspeed = 0
        self.gravity = 1
        self.collision_group = collision_group
        self.horizontal_speed = 0

    def update(self):

        horizontal_speed = 0
        onground = self.check_collisions(0, 1, self.collision_group) # Permet de définir lorsque le personnage est au sol

        key = pygame.key.get_pressed()
        # Relatif au déplacement :
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            horizontal_speed = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            horizontal_speed = self.speed
        else:
            self.image = pygame.transform.flip(self.stand_image, True, False) if self.facing_left else self.stand_image

        # Relatif au saut :
        if key[pygame.K_UP] and onground:
            self.verticalspeed = -self.jumpspeed
            self.jumping = True
            self.jump_finished = False

        if self.jumping:
            self.jump_animation()

        #Gestion de la hauteur des sauts :
        if self.previous_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.verticalspeed < -self.min_jumpspeed:
                self.verticalspeed = -self.min_jumpspeed

        if self.verticalspeed < 10 and not onground:
            self.jump_animation()
            self.verticalspeed += self.gravity


        if self.verticalspeed > 0 and onground:
            self.verticalspeed = 0

        # Relatif à l'attaque :

        if (key[pygame.K_a] and self.attack_cooldown == 0 and not self.previous_key[pygame.K_a]) or (self.previous_key[pygame.K_a] and self.attack_cooldown != 0):
            self.currently_attacking = True
            if not self.previous_key[pygame.K_a]:
                self.attack_cooldown = 60
            self.attack()
            self.attack_animation()
            horizontal_speed = 0
            self.attack_finished = False
        else:
            self.currently_attacking = False
            self.attack_index = 0
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.previous_key[pygame.K_UP] and not key[pygame.K_UP]: # Bloque le deplacement pendant l'attaque
            horizontal_speed = self.speed



        self.move(horizontal_speed, self.verticalspeed)
        self.previous_key = key



    def walk_animation(self): #Gestion de l'animation de marche
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self): #Gestion de l'animation de saut
        if not self.jump_finished:
            self.image = self.jump_images[self.jump_index]
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            self.jump_index += 1

            # Bloquer l'animation de saut pour que l'animation ne s'effectue qu'une fois lors d'un saut
            if self.jump_index == len(self.jump_images):
                self.jump_index = len(self.jump_images) - 1
                self.jump_finished = True

        else :
            self.jump_index = 0

    def attack_animation(self): #Gestion de l'animation d'attaque
        if not self.attack_finished:
            self.image = self.attack_images[self.attack_index]
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
            self.attack_index += 1

            # Bloquer l'animation d'attaque pour que l'animation ne s'effectue qu'une fois lors d'un saut
            if self.attack_index == len(self.attack_images):
                self.attack_index = len(self.attack_images) - 1
                self.attack_finished = True

        else :
            self.attack_index = 0

    def move(self, x: int, y: int): #Gestion des mouvements
        dx = x
        dy = y
        
        while self.check_collisions(0, dy, self.collision_group):
            dy -= 1 if dy > 0 else -1 if dy <0 else 0

        while self.check_collisions(dx, dy, self.collision_group):
            dx -= 1 if dx > 0 else -1 if dx < 0 else 0

        self.rect.move_ip([dx, dy])

    def attack(self): #Gestion de l'attaque
        attack_damage = 10
        attack_duration = 10
        if self.facing_left:
            attack_position = (self.rect.left - 32, self.rect.centery)
        else:
            attack_position = (self.rect.right + 32, self.rect.centery)

        # Crée une boite de collision devant le joueur qui inflige des dégats pendant une durée définie lorsqu'elle rentre au contact d'un ennemi
        attack_box = AttackBox(attack_position[0], attack_position[1], attack_damage, attack_duration)


    def check_collisions(self, x: int, y: int, collision_group):
        self.rect.move_ip([x,y]) # Déplace le joueur
        collide = pygame.sprite.spritecollideany(self, collision_group) # Vérifie les collisions
        self.rect.move_ip([-x,-y]) # Remets en place le joueur, c'est géré avant que le personnage apparaisse à l'écran donc le joueur ne remarque rien
        return collide