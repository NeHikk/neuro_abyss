import json
from game.item import Item
from game.enemy import Enemy
from game.dialogue import NPC  # убедись, что dialogue.py существует и содержит NPC

class Location:
    def __init__(self, loc_id, name, description=""):
        self.id = loc_id
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.enemies = []
        self.npcs = []  # список NPC

    def add_exit(self, direction, location):
        self.exits[direction] = location

    def get_exits(self):
        return list(self.exits.keys())

    def describe(self):
        print(f"\n--- {self.name} ---")
        print(self.description)
        if self.items:
            print("Ты видишь предметы:", ", ".join(item.name for item in self.items))
        if self.enemies:
            print("Опасность! Враги поблизости.")
        if self.npcs:
            print("Рядом есть выжившие:", ", ".join(npc.name for npc in self.npcs))
        if self.exits:
            print("Выходы:", ", ".join(self.exits.keys()))


class World:
    def __init__(self, locations_file="data/locations.json",
                 items_file="data/items.json",
                 enemies_file="data/enemies.json"):
        # Загружаем предметы и врагов
        self.items = self._load_items(items_file)
        self.enemies = self._load_enemies(enemies_file)

        # Загружаем локации (пока без связей)
        self.locations = self._load_locations(locations_file)

        # Устанавливаем связи между локациями и добавляем контент
        self._connect_locations()

    def _load_items(self, filepath):
        """Читает items.json и возвращает словарь {id: Item}."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            item_id: Item(
                name=item_data["name"],
                item_type=item_data["type"],
                description=item_data.get("description", ""),
                effect=item_data.get("effect", 0),
            )
            for item_id, item_data in data.items()
        }

    def _load_enemies(self, filepath):
        """Читает enemies.json и возвращает словарь {id: Enemy}."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            enemy_id: Enemy(
                name=enemy_data["name"],
                hp=enemy_data["hp"],
                damage=enemy_data["damage"],
                enemy_type=enemy_data.get("type", "мутант"),
            )
            for enemy_id, enemy_data in data.items()
        }

    def _load_locations(self, filepath):
        """Читает locations.json и создаёт объекты Location без связей."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            loc_id: Location(
                loc_id=loc_id,
                name=loc_data["name"],
                description=loc_data.get("description", ""),
            )
            for loc_id, loc_data in data.items()
        }

    def _connect_locations(self):
        """
        Проходим по всем локациям и для каждого выхода из JSON
        устанавливаем ссылку на объект соседней локации.
        Также добавляем предметы, врагов и NPC.
        """
        # Снова читаем locations.json, чтобы получить exits и содержимое
        with open("data/locations.json", 'r', encoding='utf-8') as f:
            data = json.load(f)

        for loc_id, loc_data in data.items():
            current_location = self.locations[loc_id]

            # Добавляем предметы
            for item_id in loc_data.get("items", []):
                if item_id in self.items:
                    current_location.items.append(self.items[item_id])

            # Добавляем врагов
            for enemy_id in loc_data.get("enemies", []):
                if enemy_id in self.enemies:
                    current_location.enemies.append(self.enemies[enemy_id])

            # Устанавливаем выходы
            for direction, target_id in loc_data.get("exits", {}).items():
                if target_id in self.locations:
                    current_location.add_exit(direction, self.locations[target_id])

            # Добавляем NPC (пока вручную для локации shelter)
            if loc_id == "shelter":
                trader = NPC("Михаил", "Торговец, который может обменять вещи.")
                # Можешь дать ему предметы для обмена, если хочешь
                # trader.inventory.append(self.items["medkit"])
                current_location.npcs.append(trader)

    def get_start_location(self, start_id="village"):
        """Возвращает стартовую локацию (по умолчанию 'village')."""
        return self.locations.get(start_id)