from nonplayablecharacter import NonPlayableCharacter
from player import Player

class Ennemy(NonPlayableCharacter):
    def __init__(self, startx: int, starty: int, collision_group, player: Player):
        super().__init__(startx, starty, collision_group, player)
        
        self.speed = 2

    def update(self):
        horizontal_speed = 0
        onground = self.check_collisions(0, 1, self.collision_group)

        player_center = self.player.rect.centerx
        ennemy_center = self.rect.centerx

        if max(player_center, ennemy_center) - min(player_center, ennemy_center)< 200:
            if player_center > ennemy_center:
                self.facing_left = False
                self.walk_animation()
                horizontal_speed = self.speed
                self.side = 'R'

            else:
                self.facing_left = True
                self.walk_animation()
                horizontal_speed = -self.speed
                self.side = 'L'


        elif self.side == 'L':
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
        if self.player_group.sprites()[0].currently_attacking == True and self.facing_left != self.player_group.sprites()[0].facing_left:
                print("Collision with player detected : NPC died")
                self.kill()
                self.dead = True

        elif self.dead == False:
            self.player_group.sprites()[0].dead = True
            print("Collision with player detected : Player died")