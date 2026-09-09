import random

def start_battle(player, enemy):
    print(f"\n=== Бой: {player.name} против {enemy.name} ===")
    while enemy.hp > 0 and player.hp > 0:
        print(f"\n{enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print(f"{player.name}: {player.hp}/{player.max_hp} HP, {player.energy} энергии")
        print("1. Атаковать")
        print("2. Использовать предмет")
        print("3. Попытаться сбежать")
        choice = input("> ").strip()
        if choice == "1":
            player.attack(enemy)
        elif choice == "2":
            if not player.inventory:
                print("Инвентарь пуст.")
                continue
            print("Предметы:")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item.name}")
            try:
                idx = int(input("Номер предмета (0 - отмена): "))
                if idx == 0:
                    continue
                item = player.inventory[idx - 1]
                player.use_item(item)
            except (ValueError, IndexError):
                print("Неверный выбор.")
                continue
        elif choice == "3":
            if random.random() < 0.5:
                print("Ты сбежал!")
                return False  # бой прерван
            else:
                print("Не получилось сбежать!")
        else:
            print("Неверный ввод.")
            continue

        if enemy.hp > 0:
            enemy.attack(player)

    if player.hp <= 0:
        print("\nТы погиб...")
        return False
    else:
        print(f"\nТы победил {enemy.name}!")
        # можно добавить лут/опыт позже
        return True