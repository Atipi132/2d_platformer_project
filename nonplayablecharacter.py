from player import Player

class NonPlayableCharacter(Player):
    def __init__(self, position, group, collision_sprites, frames):
        super().__init__(position, group, collision_sprites, frames)