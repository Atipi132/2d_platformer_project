from sprite import Sprite

class AttackBox(Sprite):
    def __init__(self, startx: int, starty: int, damage: int, duration: int):
        super().__init__("sprites/attack_box.png", startx, starty)
        self.damage = damage
        self.duration = 1
        self.lifetime = 2  # Lifetime counter

    def update(self):
        # Decrease lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Destroy the attack box when its lifetime ends