from nonplayablecharacter import NonPlayableCharacter
from player import Player
from pygame.math import Vector2 as vector

class Ennemy(NonPlayableCharacter):
    def __init__(self, position, group, collision_sprites, frames, player: Player):
        super().__init__(position, group, collision_sprites, frames)

        self.player = player

    def update(self):
        input_vector = vector(0, 0)

        player_center = self.player.rect.centerx
        ennemy_center = self.rect.centerx

        if max(player_center, ennemy_center) - min(player_center, ennemy_center) < 200:
            if player_center > ennemy_center and not self.attacking:
                self.state = "Course"
                input_vector.x += 1
                self.facing_right = True

            elif not self.attacking:
                self.facing_right = False
                self.state = "Course"
                input_vector.x -= 1
                self.facing_right = False

        elif not self.facing_right:
            if not self.on_surface["left"]:
                self.facing_right = False
                self.state = "Course"
                input_vector.x -= 1
            else:
                self.facing_right = True
                self.state = "Course"
                input_vector.x += 1

        else:
            if not self.on_surface["right"]:
                self.facing_right = True
                self.state = "Course"
                input_vector.x += 1
            else:
                self.facing_left = True
                self.state = "Course"
                input_vector.x -= 1

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        # if self.check_collisions(0, 0, self.player_group):
        #     self.player_interaction()


    # def player_interaction(self):
    #     if self.player_group.sprites()[0].currently_attacking == True and self.facing_left != self.player_group.sprites()[0].facing_left:
    #         self.dead = True
    #         print("Collision with player detected : NPC died")


    #     elif self.dead == False:
    #         self.attack_animation()
    #         self.player_group.sprites()[0].dead = True
    #         print("Collision with player detected : Player died")