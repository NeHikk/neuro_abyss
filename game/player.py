import random

class Player:
    def __init__(self, name="Алекс"):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.energy = 50          # энергия импланта
        self.max_energy = 50
        self.stability = 0        # 0..100, при 100 – ассимиляция
        self.inventory = []       # список Item
        self.weapon = None        # экипированное оружие
        self.armor = 0            # защита от брони
        self.current_location = None
        self.reputation = {}      # отношения с фракциями

    def take_damage(self, damage):
        """Получить урон с учётом брони."""
        actual = max(1, damage - self.armor)
        self.hp -= actual
        return actual

    def equip_armor(self, armor):
        """Экипировать броню."""
        self.armor = armor.effect
        print(f"Ты надеваешь {armor.name} (защита +{armor.effect}).")

    def show_status(self):
        print(f"\n=== {self.name} ===")
        print(f"Здоровье: {self.hp}/{self.max_hp}")
        print(f"Энергия: {self.energy}/{self.max_energy}")
        print(f"Стабильность: {self.stability}/100")
        if self.weapon:
            print(f"Оружие: {self.weapon.name} (урон {self.weapon.effect})")
        else:
            print("Оружие: нет (кулаки, урон 2-4)")
        if self.armor:
            print(f"Броня: защита +{self.armor}")
        if self.inventory:
            print("Инвентарь:", ", ".join(item.name for item in self.inventory))
        else:
            print("Инвентарь: пусто")

    def attack(self, enemy):
        base = self.weapon.effect if self.weapon else 3
        damage = max(1, base + random.randint(-2, 2))
        enemy.hp -= damage
        print(f"{self.name} атакует {enemy.name} и наносит {damage} урона.")
        if enemy.hp <= 0:
            print(f"{enemy.name} уничтожен!")

    def use_item(self, item):
        if item.type == "heal":
            self.hp = min(self.max_hp, self.hp + item.effect)
            print(f"Ты используешь {item.name} и восстанавливаешь {item.effect} здоровья.")
            self.inventory.remove(item)
        elif item.type == "energy":
            self.energy = min(self.max_energy, self.energy + item.effect)
            print(f"Ты используешь {item.name} и восстанавливаешь {item.effect} энергии.")
            self.inventory.remove(item)
        elif item.type == "stability":
            self.stability = max(0, self.stability - item.effect)
            print(f"Ты используешь {item.name} и снижаешь нестабильность на {item.effect}.")
            self.inventory.remove(item)
        else:
            print(f"{item.name} нельзя использовать напрямую.")

    def equip_weapon(self, weapon):
        if self.weapon:
            self.inventory.append(self.weapon)
        self.weapon = weapon
        self.inventory.remove(weapon)
        print(f"Ты экипировал {weapon.name}.")