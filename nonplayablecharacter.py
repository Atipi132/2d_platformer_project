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

    def update(self):
        horizontal_speed = 0
        onground = self.check_collisions(0, 1, self.collision_group)

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

        if not onground:
            self.verticalspeed += self.gravity

        self.move(horizontal_speed, self.verticalspeed)
        if self.check_collisions(0, 0, self.player_group):
            self.player_interaction()

    def player_interaction(self):
        pass
