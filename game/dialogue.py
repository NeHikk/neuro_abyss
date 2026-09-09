class NPC:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.inventory = []  # предметы, которые NPC может предложить для обмена

    def talk(self, player):
        """Основное взаимодействие с NPC."""
        print(f"\n{self.name}: Привет, {player.name}. Я {self.description}")
        while True:
            print("\nЧто ты хочешь?")
            print("1. Торговать")
            print("2. Уйти")
            choice = input("> ").strip()
            if choice == "1":
                self.trade(player)
            elif choice == "2":
                break
            else:
                print("Неверный выбор.")

    def trade(self, player):
        """Простой бартер: игрок может обменять предмет из своего инвентаря на предмет NPC."""
        if not self.inventory:
            print("У меня пока нет товаров для обмена.")
            return

        print("\nТвои предметы:")
        for i, item in enumerate(player.inventory, 1):
            print(f"{i}. {item.name}")

        print("\nМои предметы:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name}")

        try:
            player_choice = int(input("Выбери свой предмет (0 - отмена): "))
            if player_choice == 0:
                return
            player_item = player.inventory[player_choice - 1]

            npc_choice = int(input("Выбери мой предмет (0 - отмена): "))
            if npc_choice == 0:
                return
            npc_item = self.inventory[npc_choice - 1]

            # Меняем
            player.inventory.remove(player_item)
            self.inventory.remove(npc_item)
            player.inventory.append(npc_item)
            self.inventory.append(player_item)

            print(f"Ты обменял {player_item.name} на {npc_item.name}.")
        except (ValueError, IndexError):
            print("Ошибка выбора.")