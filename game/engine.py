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
        self.setup_game()
        self.main_loop()

    def setup_game(self):
        print("=== НейроБездна ===")
        name = input("Введи имя героя (по умолчанию Алекс): ").strip() or "Алекс"
        self.player = Player(name)
        self.world = World()
        self.player.current_location = self.world.get_start_location()

    def main_loop(self):
        while self.running and self.player.hp > 0:
            loc = self.player.current_location
            loc.describe()

            # Обработка врагов
            if loc.enemies:
                enemy = loc.enemies[0]
                print(f"На тебя нападает {enemy.name}!")
                if result := start_battle(self.player, enemy):
                    loc.enemies.remove(enemy)
                    if not loc.enemies:
                        print("Врагов больше нет.")
                elif self.player.hp <= 0:
                    break
                else:
                    continue

            # Меню действий
            print("\nЧто делаешь?")
            options = ["1. Идти (переместиться)", "2. Осмотреться", "3. Подобрать предметы", "4. Проверить статус"]
            if loc.npcs:
                options.append("5. Поговорить с выжившим")
            options.append("6. Выйти из игры")
            for opt in options:
                print(opt)

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

    def talk_to_npc(self, npc):
        npc.talk(self.player)

    # Остальные методы move, look_closer, pickup_items без изменений...