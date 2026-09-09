import random

class Enemy:
    def __init__(self, name, hp, damage, enemy_type="мутант"):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.enemy_type = enemy_type   # мутант, бандит, дрон, босс

    def attack(self, player):
        dealt = max(1, self.damage + random.randint(-2, 2))
        player.hp -= dealt
        print(f"{self.name} атакует и наносит {dealt} урона.")

    def is_alive(self):
        return self.hp > 0