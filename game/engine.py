from game.player import Player
from game.item import Item
from game.enemy import Enemy
from game.location import Location
from game.battle import start_battle
import random

class Game:
    def __init__(self):
        self.running = True
        self.player = None

    def run(self):
        self.setup_game()
        self.main_loop()

    def setup_game(self):
        print("=== НейроБездна ===")
        name = input("Введи имя героя (по умолчанию Алекс): ").strip() or "Алекс"
        self.player = Player(name)

        # Локации
        village = Location(
            "Разрушенная деревня",
            "Ты стоишь посреди того, что когда-то было деревней. Вокруг обгоревшие дома, а в воздухе висит запах гари."
        )
        forest = Location(
            "Тёмный лес",
            "Густые деревья почти не пропускают свет. Где-то вдалеке слышен треск."
        )
        bunker = Location(
            "Старый бункер",
            "Тяжёлая металлическая дверь ведёт внутрь. Внутри темно, но есть признаки недавнего пребывания людей."
        )

        # Связи
        village.add_exit("север", forest)
        village.add_exit("запад", bunker)
        forest.add_exit("юг", village)
        bunker.add_exit("восток", village)

        # Предметы
        village.items.append(Item("Аптечка", "heal", "Восстанавливает 20 здоровья", 20))
        village.items.append(Item("Батарея", "energy", "Восстанавливает 25 энергии", 25))
        forest.items.append(Item("Старый пистолет", "weapon", "Пистолет, урон 8", 8))
        forest.enemies.append(Enemy("Порченый волк", 30, 8, "мутант"))
        bunker.items.append(Item("Антирад", "stability", "Снижает нестабильность на 15", 15))
        bunker.enemies.append(Enemy("Бандит", 40, 10, "бандит"))

        self.player.current_location = village

    def main_loop(self):
        while self.running and self.player.hp > 0:
            loc = self.player.current_location
            loc.describe()

            # Если есть враги, автоматически начинаем бой с первым
            if loc.enemies:
                enemy = loc.enemies[0]
                print(f"На тебя нападает {enemy.name}!")
                if result := start_battle(self.player, enemy):
                    loc.enemies.remove(enemy)
                    if not loc.enemies:
                        print("Врагов больше нет.")
                elif self.player.hp <= 0:
                    break  # игрок погиб
                else:
                    # если сбежал, враг остаётся, но продолжать можно
                    continue

            print("\nЧто делаешь?")
            print("1. Идти (переместиться)")
            print("2. Осмотреться (подробнее)")
            print("3. Подобрать предметы")
            print("4. Проверить статус")
            print("5. Выйти из игры")
            choice = input("> ").strip()

            if choice == "1":
                self.move()
            elif choice == "2":
                self.look_closer()
            elif choice == "3":
                self.pickup_items()
            elif choice == "4":
                self.player.show_status()
            elif choice == "5":
                self.running = False
                print("Игра завершена.")
            else:
                print("Неверный ввод.")

        if self.player.hp <= 0:
            print("\nИгра окончена. Ты погиб.")

    def move(self):
        loc = self.player.current_location
        if not loc.exits:
            print("Некуда идти.")
            return
        print("Куда идти?")
        for direction in loc.exits:
            print(f"- {direction}")
        direction = input("Направление: ").strip().lower()
        if direction in loc.exits:
            self.player.current_location = loc.exits[direction]
        else:
            print("Туда нельзя идти.")

    def look_closer(self):
        loc = self.player.current_location
        print(loc.description)
        if loc.items:
            print("Предметы:", ", ".join(item.name for item in loc.items))
        else:
            print("Предметов нет.")
        if loc.enemies:
            print("Враги:", ", ".join(enemy.name for enemy in loc.enemies))
        else:
            print("Врагов не видно.")

    def pickup_items(self):
        loc = self.player.current_location
        if not loc.items:
            print("Здесь нечего подбирать.")
            return
        print("Что подобрать?")
        for idx, item in enumerate(loc.items, 1):
            print(f"{idx}. {item.name}")
        print("0. Ничего")
        try:
            choice = int(input("> "))
        except ValueError:
            print("Нужно ввести число.")
            return
        if 1 <= choice <= len(loc.items):
            item = loc.items.pop(choice - 1)
            self.player.inventory.append(item)
            print(f"Ты подобрал {item.name}.")
        elif choice != 0:
            print("Неверный номер.")