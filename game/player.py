import random
import json
from rich.console import Console
from rich.panel import Panel

console = Console()


class Player:
    def __init__(self, name="Алекс"):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.energy = 50  # энергия импланта
        self.max_energy = 50
        self.stability = 0  # 0..100, при 100 – ассимиляция
        self.inventory = []  # список Item
        self.weapon = None  # экипированное оружие
        self.armor = 0  # защита от брони
        self.current_location = None
        self.reputation = {}  # отношения с фракциями

    def take_damage(self, damage):
        """Получить урон с учётом брони."""
        actual = max(1, damage - self.armor)
        self.hp -= actual
        return actual

    def equip_armor(self, armor):
        """Экипировать броню."""
        self.armor = armor.effect
        console.print(f"[green]Ты надеваешь {armor.name} (защита +{armor.effect}).[/green]")

    def show_status(self):
        """Красивый вывод статуса с прогресс-барами."""
        hp_percent = int((self.hp / self.max_hp) * 100)
        stab_percent = self.stability

        # Прогресс-бары
        hp_bar = "█" * (hp_percent // 5) + "░" * (20 - hp_percent // 5)
        stab_bar = "█" * (stab_percent // 5) + "░" * (20 - stab_percent // 5)

        # Цвет стабильности в зависимости от значения
        if stab_percent < 50:
            stab_color = "green"
        elif stab_percent < 80:
            stab_color = "yellow"
        else:
            stab_color = "red"

        status_text = (
            f"[red]ЗДОРОВЬЕ[/red]      {hp_bar} [bold]{hp_percent}%[/bold]\n"
            f"[{stab_color}]СТАБИЛЬНОСТЬ[/{stab_color}] {stab_bar} [bold]{stab_percent}%[/bold]\n"
            f"[yellow]ЭНЕРГИЯ[/yellow]       {'█' * (self.energy // 5)}{'░' * (20 - self.energy // 5)} [bold]{self.energy}/{self.max_energy}[/bold]\n\n"
            f"[cyan]Оружие:[/cyan] {self.weapon.name + ' (урон ' + str(self.weapon.effect) + ')' if self.weapon else '[dim]Кулаки (урон 2-4)[/dim]'}\n"
            f"[cyan]Броня:[/cyan]  +{self.armor}\n"
        )

        if self.inventory:
            status_text += "\n[bold green]ИНВЕНТАРЬ:[/bold green]\n"
            for item in self.inventory:
                status_text += f"  • {item.name}\n"
        else:
            status_text += "\n[dim italic]Инвентарь пуст[/dim italic]"

        console.print(Panel(status_text, title=f" ДАЙВЕР: {self.name.upper()} ", border_style="cyan", expand=False))

    def attack(self, enemy):
        base = self.weapon.effect if self.weapon else 3
        damage = max(1, base + random.randint(-2, 2))
        enemy.hp -= damage
        console.print(f"[yellow]{self.name}[/yellow] атакует [red]{enemy.name}[/red] и наносит [bold]{damage}[/bold] урона.")
        if enemy.hp <= 0:
            console.print(f"[green]{enemy.name} уничтожен![/green]")

    def use_item(self, item):
        if item.type == "heal":
            self.hp = min(self.max_hp, self.hp + item.effect)
            console.print(f"[green]Ты используешь {item.name} и восстанавливаешь {item.effect} здоровья.[/green]")
            self.inventory.remove(item)
        elif item.type == "energy":
            self.energy = min(self.max_energy, self.energy + item.effect)
            console.print(f"[yellow]Ты используешь {item.name} и восстанавливаешь {item.effect} энергии.[/yellow]")
            self.inventory.remove(item)
        elif item.type == "stability":
            self.stability = max(0, self.stability - item.effect)
            console.print(f"[magenta]Ты используешь {item.name} и снижаешь нестабильность на {item.effect}.[/magenta]")
            self.inventory.remove(item)
        else:
            console.print(f"[red]{item.name} нельзя использовать напрямую.[/red]")

    def equip_weapon(self, weapon):
        if self.weapon:
            self.inventory.append(self.weapon)
        self.weapon = weapon
        if weapon in self.inventory:
            self.inventory.remove(weapon)
        console.print(f"[green]Ты экипировал {weapon.name}.[/green]")

    def save_game(self, filename="save.json"):
        """Сохраняет состояние игрока в JSON."""
        data = {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "energy": self.energy,
            "max_energy": self.max_energy,
            "stability": self.stability,
            "armor": self.armor,
            "current_location_id": self.current_location.id if self.current_location else "village",
            "inventory_items": [item.name for item in self.inventory],
            "weapon_name": self.weapon.name if self.weapon else None,
            "reputation": self.reputation
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        console.print("\n[bold green]✓ Игра успешно сохранена![/bold green]")

    def load_game(self, filename="save.json", world=None):
        """Загружает состояние игрока из JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.name = data["name"]
            self.hp = data["hp"]
            self.max_hp = data["max_hp"]
            self.energy = data["energy"]
            self.max_energy = data["max_energy"]
            self.stability = data["stability"]
            self.armor = data["armor"]
            self.reputation = data.get("reputation", {})

            # Восстанавливаем локацию
            if world:
                location_id = data.get("current_location_id", "village")
                self.current_location = world.locations.get(location_id)

            # Восстанавливаем инвентарь
            if world:
                self.inventory = []
                for item_name in data.get("inventory_items", []):
                    # Ищем предмет по имени в мире
                    for item_id, item in world.items.items():
                        if item.name == item_name:
                            self.inventory.append(item)
                            break

            # Восстанавливаем оружие
            if world and data.get("weapon_name"):
                weapon_name = data["weapon_name"]
                for item_id, item in world.items.items():
                    if item.name == weapon_name and item.type == "weapon":
                        self.weapon = item
                        break

            console.print(f"\n[bold green]✓ Игра загружена! Добро пожаловать обратно, {self.name}.[/bold green]")
            return True
        except FileNotFoundError:
            console.print("[red]✗ Файл сохранения не найден.[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Ошибка загрузки: {e}[/red]")
            return False