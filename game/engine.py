from game.player import Player
from game.location import World
from game.battle import start_battle
from game.dialogue import NPC
import random


class Game:
    def __init__(self):
        self.running = True
        self.player = None
        self.world = None

    def run(self):
        """Точка входа: настройка игры и запуск основного цикла."""
        self.setup_game()
        self.main_loop()

    def setup_game(self):
        """Создаём игрока и загружаем мир из JSON."""
        print("=== НейроБездна ===")
        name = input("Введи имя героя (по умолчанию Алекс): ").strip() or "Алекс"
        self.player = Player(name)
        self.world = World()
        self.player.current_location = self.world.get_start_location()

    def main_loop(self):
        """Основной игровой цикл."""
        while self.running and self.player.hp > 0:
            loc = self.player.current_location
            loc.describe()

            # --- Бой с врагами, если они есть в локации ---
            if loc.enemies:
                enemy = loc.enemies[0]
                print(f"На тебя нападает {enemy.name}!")
                if start_battle(self.player, enemy):
                    loc.enemies.remove(enemy)
                    if not loc.enemies:
                        print("Врагов больше нет.")
                elif self.player.hp <= 0:
                    break
                else:
                    # Игрок сбежал — пропускаем остальные действия на этот ход
                    continue

            # --- Меню действий ---
            print("\nЧто делаешь?")
            options = [
                "1. Идти",
                "2. Осмотреться",
                "3. Подобрать предметы",
                "4. Проверить статус",
            ]
            if loc.npcs:
                options.append("5. Поговорить с выжившим")
            options.append("6. Выйти из игры")
            for o in options:
                print(o)

            choice = input("> ").strip()

            if choice == "1":
                self.move()
            elif choice == "2":
                self.look_closer()
            elif choice == "3":
                self.pickup_items()
            elif choice == "4":
                self.player.show_status()
            elif choice == "5" and loc.npcs:
                self.talk_to_npc(loc.npcs[0])
            elif choice == "6":
                self.running = False
                print("Игра завершена.")
            else:
                print("Неверный ввод.")

        if self.player.hp <= 0:
            print("\nИгра окончена. Ты погиб.")

    # ------------------- Вспомогательные методы -------------------

    def move(self):
        """Перемещение между локациями."""
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
        """Подробный осмотр локации."""
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
        if loc.npcs:
            print("Выжившие:", ", ".join(npc.name for npc in loc.npcs))

    def pickup_items(self):
        """Подбор предметов с автоэкипировкой оружия и брони."""
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

            # Логика автоэкипировки
            if item.type == "weapon" and self.player.weapon is None:
                self.player.weapon = item
                print(f"Ты подобрал и сразу экипировал {item.name}.")
            elif item.type == "armor":
                self.player.equip_armor(item)
                print(f"Ты подобрал {item.name}.")
            else:
                self.player.inventory.append(item)
                print(f"Ты подобрал {item.name}.")
        elif choice != 0:
            print("Неверный номер.")

    def talk_to_npc(self, npc):
        """Разговор с NPC."""
        npc.talk(self.player)