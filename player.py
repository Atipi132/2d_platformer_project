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
        self.walk_cycle = [pygame.image.load("sprites/RedHoodSprite/Course/RedHood-Course ({}).png".format(i)) for i in range(1, 48)]
        self.animation_index = 0
        self.facing_left = False
        self.speed = 5

        self.dead = False
        self.previous_key = pygame.key.get_pressed()
        self.verticalspeed = 0
        self.gravity = 1
        self.collision_group = collision_group

    def update(self):

        horizontal_speed = 0
        onground = self.check_collisions(0, 1, self.collision_group)

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            horizontal_speed = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            horizontal_speed = self.speed
        else:
            self.image = self.stand_image if self.facing_left == False else pygame.transform.flip(self.stand_image, True, False)

        if key[pygame.K_UP] and onground:
            self.verticalspeed = -self.jumpspeed
            self.jumping = True
            self.jump_finished = False

        if (key[pygame.K_a] and self.attack_cooldown == 0 and not self.previous_key[pygame.K_a]) or (self.previous_key[pygame.K_a] and self.attack_cooldown != 0):
            self.currently_attacking = True
            if not self.previous_key[pygame.K_a]:
                self.attack_cooldown = 15
            self.attack()
            self.attack_animation()
            horizontal_speed = 0
            self.attack_finished = False
        else:
            self.currently_attacking = False
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.jumping:
            self.jump_animation()

        if self.previous_key[pygame.K_UP] and not key[pygame.K_UP]: # bloque le deplacement pendant l'attaque
            horizontal_speed = self.speed

        # variable height jumping
        if self.previous_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.verticalspeed < -self.min_jumpspeed:
                self.verticalspeed = -self.min_jumpspeed
        self.previous_key = key


        if self.verticalspeed < 10 and not onground:
            self.jump_animation()
            self.verticalspeed += self.gravity


        if self.verticalspeed > 0 and onground:
            self.verticalspeed = 0

        self.move(horizontal_speed, self.verticalspeed)


    def walk_animation(self):
        self.image = pygame.transform.flip(self.walk_cycle[self.animation_index], True, False) if self.facing_left else self.walk_cycle[self.animation_index]

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        if not self.jump_finished:
            self.image = self.jump_images[self.jump_index]
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
            self.jump_index += 1


            if self.jump_index >= len(self.jump_images):
                self.jump_index = len(self.jump_images) - 1
                self.jump_finished = True
        else :
            self.jump_index = 0

    def attack_animation(self):
        if not self.attack_finished:
            self.image = self.attack_images[self.attack_index]
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)
            self.attack_index += 1

            if self.attack_index >= len(self.attack_images):
                self.attack_index = len(self.attack_images) - 1
                self.attack_finished = True
        if self.attack_finished:
            self.attack_index = 0

    def move(self, x: int, y: int):
        dx = x
        dy = y
        
        while self.check_collisions(0, dy, self.collision_group):
            dy -= 1 if dy > 0 else -1 if dy <0 else 0

        while self.check_collisions(dx, dy, self.collision_group):
            dx -= 1 if dx > 0 else -1 if dx < 0 else 0

        self.rect.move_ip([dx, dy])

    def attack(self):
        # Create an attack box in front of the player
        attack_damage = 10
        attack_duration = 10
        if self.facing_left:
            attack_position = (self.rect.left - 32, self.rect.centery)
        else:
            attack_position = (self.rect.right + 32, self.rect.centery)

        attack_box = AttackBox(attack_position[0], attack_position[1], attack_damage, attack_duration)


    def check_collisions(self, x: int, y: int, collision_group):
        self.rect.move_ip([x,y]) # move the player
        collide = pygame.sprite.spritecollideany(self, collision_group) # check for collision
        self.rect.move_ip([-x,-y]) # move the player back to the original coordinates ; all of this is done before the player is drawn to the screen so the user doesn't see anything
        return collide