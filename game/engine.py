import time
import random
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from game.player import Player
from game.location import World
from game.battle import start_battle
from game.dialogue import NPC

console = Console()


class Game:
    def __init__(self):
        self.running = True
        self.player = None
        self.world = None
        self.save_file = "save.json"

    def show_intro(self):
        """Выводит стильное вступление с лором игры."""
        title = Text("""
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
        """, style="bold cyan")

        console.print(Panel(title, border_style="blue", title="NEURO ABYSS v1.0"))

        lore_text = (
            "[bold red]2147 год.[/bold red] Мир утонул в собственных мыслях.\n"
            "Проект «Бездна» должен был даровать бессмертие, но стал цифровым чистилищем.\n"
            "Те, чей разум не выдержал синхронизации, стали [bold yellow]Ассимилированными[/bold yellow] —\n"
            "пустыми оболочками, движимыми искаженными алгоритмами.\n\n"
            "Ты — [bold cyan]Дайвер[/bold cyan]. Твой нейроимплант обладает редкой устойчивостью\n"
            "к шепоту Бездны. Твоя [bold magenta]Стабильность[/bold magenta] — это грань\n"
            "между разумом и вечным безумием.\n\n"
            "[italic]Цель: выжить, найти источник сигнала и не потерять себя.[/italic]"
        )
        console.print(Panel(lore_text, border_style="dim", expand=False))

        time.sleep(1)
        console.print("\n[blink]Нажми Enter, чтобы инициировать нейроподключение...[/blink]", end="")
        console.input()
        console.clear()

    def run(self):
        """Точка входа: показ интро, настройка игры и запуск основного цикла."""
        self.show_intro()
        
        # Предлагаем загрузить сохранение
        if os.path.exists(self.save_file):
            console.print("\n[yellow]Обнаружен файл сохранения.[/yellow]")
            load_choice = console.input("[cyan]Загрузить сохраненную игру? (y/n): [/cyan]").strip().lower()
            if load_choice == 'y':
                self.world = World()
                self.player = Player()
                if self.player.load_game(self.save_file, self.world):
                    self.main_loop()
                    return
                else:
                    console.print("[red]Не удалось загрузить игру. Начинаем новую...[/red]")
        
        # Если не загружаем, начинаем новую игру
        self.setup_game()
        self.main_loop()

    def setup_game(self):
        """Создаём игрока и загружаем мир из JSON."""
        name = console.input("[cyan]Введи позывной Дайвера (по умолчанию Алекс): [/cyan]").strip() or "Алекс"
        self.player = Player(name)
        self.world = World()
        self.player.current_location = self.world.get_start_location()

        console.print(f"\n[bold green][СИСТЕМА][/bold green]: Нейроинтерфейс активирован. Добро пожаловать, [cyan]{self.player.name}[/cyan].")
        console.print("[bold green][СИСТЕМА][/bold green]: Уровень стабильности в норме. Начинаем сканирование локации...\n")

    def main_loop(self):
        """Основной игровой цикл."""
        while self.running and self.player.hp > 0:
            loc = self.player.current_location
            loc.describe()

            # --- Бой с врагами, если они есть в локации ---
            if loc.enemies:
                enemy = loc.enemies[0]
                console.print(f"\n[bold red]⚠ НА ПАДАЕТ {enemy.name.upper()}! ⚠[/bold red]")
                if start_battle(self.player, enemy):
                    loc.enemies.remove(enemy)
                    if not loc.enemies:
                        console.print("[green]Врагов больше нет.[/green]")
                elif self.player.hp <= 0:
                    break
                else:
                    continue

            # --- Меню действий ---
            console.print("\n[bold cyan]═══ ЧТО ДЕЛАЕШЬ? ═══[/bold cyan]")
            options = [
                "[yellow]1.[/yellow] Идти",
                "[yellow]2.[/yellow] Осмотреться",
                "[yellow]3.[/yellow] Подобрать предметы",
                "[yellow]4.[/yellow] Проверить статус",
                "[yellow]7.[/yellow] Сохранить игру",
            ]
            if loc.npcs:
                options.append("[yellow]5.[/yellow] Поговорить с выжившим")
            options.append("[yellow]6.[/yellow] Выйти из игры")

            for o in options:
                console.print(o)

            choice = console.input("\n[bold cyan]> [/bold cyan]").strip()

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
                console.print("\n[bold yellow]Игра завершена. До встречи в Бездне...[/bold yellow]")
            elif choice == "7":
                self.player.save_game(self.save_file)
            else:
                console.print("[red]Неверный ввод.[/red]")

        if self.player.hp <= 0:
            console.print("\n[bold red]═══ ИГРА ОКОНЧЕНА ═══[/bold red]")
            console.print("[red]Ты погиб. Бездна поглотила твой разум...[/red]")

    # ------------------- Вспомогательные методы -------------------
    def move(self):
        """Перемещение между локациями."""
        loc = self.player.current_location
        if not loc.exits:
            console.print("[red]Некуда идти.[/red]")
            return

        console.print("\n[cyan]Куда идти?[/cyan]")
        for direction in loc.exits:
            console.print(f"  • [yellow]{direction}[/yellow]")
        direction = console.input("[cyan]Направление: [/cyan]").strip().lower()
        if direction in loc.exits:
            self.player.current_location = loc.exits[direction]
            console.print(f"\n[green]Ты перемещаешься в новую локацию...[/green]")
        else:
            console.print("[red]Туда нельзя идти.[/red]")

    def look_closer(self):
        """Подробный осмотр локации."""
        loc = self.player.current_location
        console.print(f"\n[dim italic]{loc.description}[/dim italic]")

        if loc.items:
            console.print("[cyan]Предметы:[/cyan] " + ", ".join(item.name for item in loc.items))
        else:
            console.print("[dim]Предметов нет.[/dim]")

        if loc.enemies:
            console.print("[red]Враги:[/red] " + ", ".join(enemy.name for enemy in loc.enemies))
        else:
            console.print("[dim]Врагов не видно.[/dim]")

        if loc.npcs:
            console.print("[green]Выжившие:[/green] " + ", ".join(npc.name for npc in loc.npcs))

    def pickup_items(self):
        """Подбор предметов с автоэкипировкой оружия и брони."""
        loc = self.player.current_location
        if not loc.items:
            console.print("[red]Здесь нечего подбирать.[/red]")
            return

        console.print("\n[cyan]Что подобрать?[/cyan]")
        for idx, item in enumerate(loc.items, 1):
            console.print(f"  [yellow]{idx}.[/yellow] {item.name}")
        console.print("  [yellow]0.[/yellow] Ничего")

        try:
            choice = int(console.input("[cyan]> [/cyan]"))
        except ValueError:
            console.print("[red]Нужно ввести число.[/red]")
            return

        if 1 <= choice <= len(loc.items):
            item = loc.items.pop(choice - 1)
            if item.type == "weapon" and self.player.weapon is None:
                self.player.weapon = item
                console.print(f"[green]Ты подобрал и сразу экипировал {item.name}.[/green]")
            elif item.type == "armor":
                self.player.equip_armor(item)
                console.print(f"[green]Ты подобрал {item.name}.[/green]")
            else:
                self.player.inventory.append(item)
                console.print(f"[green]Ты подобрал {item.name}.[/green]")
        elif choice != 0:
            console.print("[red]Неверный номер.[/red]")

    def talk_to_npc(self, npc):
        """Разговор с NPC."""
        npc.talk(self.player)