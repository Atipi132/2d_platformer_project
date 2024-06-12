from settings import *
import pygame
from pygame.math import Vector2 as vector
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], group : pygame.sprite.Group, collision_sprites : pygame.sprite.Group, frames):
        super().__init__(group)

        # image
        self.frames, self.frame_index = frames, 0
        self.state = 'Idle'
        self.facing_right = True
        self.image = self.frames[self.state][self.frame_index]

        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()

        # movement
        self.direction = vector()
        self.speed = 10
        self.gravity = 3
        self.jump = False
        self.previousJump = False
        self.jump_height = 30

        self.attacking = False
        self.attack_position = (self.rect.left - 32, self.rect.centery)

        self.attacking = False

        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.platform = None
        self.dead = False

        self.timers = {
            'attack duration': Timer(400),
        }

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.dead:
            input_vector = vector(0, 0)

            if not keys[pygame.K_UP]:
                self.previousJump = False

            if keys[pygame.K_RIGHT]:
                if not self.attacking :
                    input_vector.x += 1
                    self.facing_right = True

            if keys[pygame.K_LEFT]:
                if not self.attacking:
                    input_vector.x -= 1
                    self.facing_right = False

            if keys[pygame.K_a]:
                self.attack()

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

            if keys[pygame.K_UP] and not self.previousJump:
                self.previousJump = True
                self.jump = True

    def move(self, timeF):
        if not self.dead:
            # horizontal
            self.rect.x += self.direction.x * self.speed * timeF
            self.collision('horizontal')

            # vertical
            self.direction.y += self.gravity/2 * timeF
            self.rect.y += self.direction.y * timeF
            self.direction.y += self.gravity/2 *timeF
            self.collision('vertical')

            if self.jump:
                if self.on_surface['floor']:
                    self.direction.y = -self.jump_height
                self.jump = False

    def attack(self):
        if not self.timers['attack duration'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack duration'].activate()

        attack_damage = 10
        attack_duration = 10
        if self.facing_right:
            self.attack_position = (self.rect.left + 32, self.rect.centery)
        else:
            self.attack_position = (self.rect.right - 32, self.rect.centery)

    def collision(self, axis: str):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect) :
                if axis == 'horizontal':
                    # Gauche
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.rect.left = sprite.rect.right
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")
                    # Droite
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.rect.right = sprite.rect.left
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")

                if axis == 'vertical' :
                    # Top
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")
                    # Bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom <= sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")
                    self.direction.y = 0

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4),
                                 (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4),
                                (2, self.rect.height / 2))

        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # collisions
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False


    def animate(self, timeF):
        self.frame_index += ANIMATION_SPEED * timeF
        if self.state == 'Attaque' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'Idle'
        if self.state == 'Saut' and self.frame_index == len(self.frames[self.state]):
            self.state = 'Chute'
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False



    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'Attaque'
            else:
                self.state = 'Idle' if self.direction.x == 0 else 'Course'
        else:
            self.state = 'Saut' if self.direction.y < 0 else 'Chute'

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, timeF):
        self.old_rect = self.rect.copy()
        self.update_timers()

        self.input()
        self.move(timeF)
        self.check_contact()
        self.get_state()
        self.animate(timeF)