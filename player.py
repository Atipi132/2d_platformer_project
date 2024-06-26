from settings import *
import pygame
from pygame.math import Vector2 as vector
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], group : pygame.sprite.Group, collision_sprites : pygame.sprite.Group, frames):
        super().__init__(group)

        # Image and sprites of the player :
        self.frames, self.frame_index = frames, 0
        self.state = 'Idle'
        self.facing_right = True
        self.image = self.frames[self.state][self.frame_index]

        # Relative to the collision :
        self.rect = self.image.get_rect(topleft=position)
        self.old_rect = self.rect.copy()
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}

        # Relative to the movement of the player :
        self.direction = vector()
        self.speed = 10
        self.gravity = 3
        self.jump = False
        self.JumpKeyReleased = False
        self.jump_height = 30

        # Relative to the attack :
        self.attacking = False
        self.AttackKeyReleased = False
        self.attack_position = (self.rect.left - 32, self.rect.centery)

        self.platform = None

        self.dead = False

        # Timers for various actions
        self.timers = {
            'attack duration': Timer(400),
        }

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.dead:
            input_vector = vector(0, 0)

            # Check for right movement
            if keys[pygame.K_RIGHT]:
                if not self.attacking:
                    input_vector.x += 1
                    self.facing_right = True

            # Check for left movement
            if keys[pygame.K_LEFT]:
                if not self.attacking:
                    input_vector.x -= 1
                    self.facing_right = False

            # Check if the player is holding the attack key
            if not keys[pygame.K_a]:
                self.AttackKeyReleased = False

            # Check for attack action
            if keys[pygame.K_a] and not self.AttackKeyReleased:
                self.attack()
                self.AttackKeyReleased = True

            # Check if the player is not holding the jump key
            if not keys[pygame.K_UP]:
                self.JumpKeyReleased = False

            # Check for jump action
            if keys[pygame.K_UP] and not self.JumpKeyReleased:
                self.JumpKeyReleased = True
                self.jump = True

            # Normalize the input vector for consistent speed
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def move(self, GameTime):
        if not self.dead:
            # Horizontal movement and collision
            self.rect.x += self.direction.x * self.speed * GameTime
            self.collision('horizontal')

            # Apply gravity for vertical movement and vertical collision
            self.direction.y += self.gravity/2 * GameTime
            self.rect.y += self.direction.y * GameTime
            self.direction.y += self.gravity/2 * GameTime
            self.collision('vertical')

            # Handle jumping
            if self.jump:
                if self.on_surface['floor']:
                    self.direction.y = -self.jump_height
                self.jump = False

    def attack(self):
        if not self.timers['attack duration'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack duration'].activate()

        # Set attack position based on facing direction
        if self.facing_right:
            self.attack_position = (self.rect.left + 32, self.rect.centery)
        else:
            self.attack_position = (self.rect.right - 32, self.rect.centery)

    def collision(self, axis: str):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # Collision with the left
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.rect.left = sprite.rect.right
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")
                    # Collision with the right
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.rect.right = sprite.rect.left
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")

                if axis == 'vertical':
                    # Collision with the top
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")
                    # Collision with the bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom <= sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                        if sprite.image == pygame.image.load("sprites\\Plateforme\\Starter Tiles Platformer\\DarkCastleTiles\\DarkCastle_9_16x16.png"):
                            print("door collision detected")
                    self.direction.y = 0

    def check_contact(self):
        # Define rectangles for floor, right, and left contact detection
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2)) # Create a rectangle at the bottom, it will be used for the floor collision
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), # Create a rectangle at the topright, it will be used for the right collision
                                 (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), # Create a rectangle at the topleft, it will be used for the left collision
                                (2, self.rect.height / 2))

        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # # Check for collisions and update surface contact status
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

    def animate(self, GameTime):
        # Update frame index based on animation speed
        self.frame_index += ANIMATION_SPEED * GameTime
        if self.state == 'Attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'Idle'
        if self.state == 'Jump' and self.frame_index == len(self.frames[self.state]):
            self.state = 'Fall'
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

    def get_state(self):
        # Update the player's state based on their current actions and position
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'Attack'
            else:
                self.state = 'Idle' if self.direction.x == 0 else 'Run'
        else:
            self.state = 'Jump' if self.direction.y < 0 else 'Fall'

    def update_timers(self):
        # Update all timers
        for timer in self.timers.values():
            timer.update()

    def update(self, GameTime):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(GameTime)
        self.check_contact()
        self.get_state()
        self.animate(GameTime)