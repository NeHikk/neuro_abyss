class NPC:
    """Базовый класс для всех NPC."""
    def __init__(self, npc_id, name, npc_type, description="", dialogue=""):
        self.id = npc_id
        self.name = name
        self.type = npc_type   # trader, quest_giver, crafter, simple
        self.description = description
        self.dialogue = dialogue
        self.inventory = []

    def talk(self, player):
        """Основное взаимодействие."""
        print(f"\n{self.name}: {self.dialogue}")

        while True:
            print(f"\n--- Разговор с {self.name} ---")
            print("1. Продолжить разговор")
            if self.type == "trader":
                print("2. Торговать")
            elif self.type == "crafter":
                print("2. Улучшить оружие")
            print("0. Уйти")
            choice = input("> ").strip()

            if choice == "1":
                self.small_talk()
            elif choice == "2" and self.type == "trader":
                self.trade(player)
            elif choice == "2" and self.type == "crafter":
                self.craft(player)
            elif choice == "0":
                print(f"Ты прощаешься с {self.name}.")
                break
            else:
                print("Неверный выбор.")

    def small_talk(self):
        """Дополнительные реплики для атмосферы."""
        if self.type == "quest_giver":
            print(f"{self.name}: Береги себя, Хранитель. Бездна не дремлет.")
        elif self.type == "trader":
            print(f"{self.name}: Товар — это единственное, что имеет цену в этом мире.")
        elif self.type == "crafter":
            print(f"{self.name}: Металл и код — вот что держит нас на плаву.")
        elif self.type == "simple":
            print(f"{self.name}: Ты ещё не понял? Всё вокруг — иллюзия Бездны.")
        else:
            print(f"{self.name}: Хм...")

    def trade(self, player):
        """Простой бартер."""
        if not self.inventory:
            print("У меня нет товаров.")
            return

        print("\nТвои предметы:")
        for i, item in enumerate(player.inventory, 1):
            print(f"{i}. {item.name}")

        print("\nМои предметы:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name} (эффект: {item.effect})")

        try:
            pc = input("Выбери свой предмет (0 - отмена): ")
            if pc == "0":
                return
            player_item = player.inventory[int(pc) - 1]

            nc = input("Выбери мой предмет (0 - отмена): ")
            if nc == "0":
                return
            npc_item = self.inventory[int(nc) - 1]

            player.inventory.remove(player_item)
            self.inventory.remove(npc_item)
            player.inventory.append(npc_item)
            self.inventory.append(player_item)

            print(f"Ты обменял {player_item.name} на {npc_item.name}.")
        except (ValueError, IndexError):
            print("Ошибка выбора.")

    def craft(self, player):
        """Улучшение оружия (упрощённо: обмен 3 металлолома на +2 урона)."""
        scrap_count = len([item for item in player.inventory if item.name == "Металлолом"])
        if scrap_count < 3:
            print(f"Нужно 3 металлолома, у тебя {scrap_count}. Принеси ещё.")
            return

        if not player.weapon:
            print("У тебя нет оружия в руках. Экипируй что-нибудь.")
            return

        # Удаляем 3 металлолома
        removed = 0
        for item in list(player.inventory):
            if item.name == "Металлолом" and removed < 3:
                player.inventory.remove(item)
                removed += 1

        player.weapon.effect += 2
        print(f"{self.name} улучшает {player.weapon.name}! Теперь урон {player.weapon.effect}.")