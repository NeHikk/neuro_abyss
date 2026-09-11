import json
import os
from game.item import Item
from game.enemy import Enemy
from game.dialogue import NPC

# Определяем корень проекта (папка, где лежит main.py и data/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


class Location:
    def __init__(self, loc_id, name, description=""):
        self.id = loc_id
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.enemies = []
        self.npcs = []

    def add_exit(self, direction, location):
        self.exits[direction] = location

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
    def __init__(self,
                 locations_file=os.path.join(DATA_DIR, "locations.json"),
                 items_file=os.path.join(DATA_DIR, "items.json"),
                 enemies_file=os.path.join(DATA_DIR, "enemies.json"),
                 npcs_file=os.path.join(DATA_DIR, "npcs.json")):
        self.items = self._load_items(items_file)
        self.enemies = self._load_enemies(enemies_file)
        self.npcs = self._load_npcs(npcs_file)
        self.locations = self._load_locations(locations_file)
        self._connect_locations()

    def _load_items(self, filepath):
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
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            enemy_id: Enemy(
                name=ed["name"],
                hp=ed["hp"],
                damage=ed["damage"],
                enemy_type=ed.get("type", "мутант"),
            )
            for enemy_id, ed in data.items()
        }

    def _load_npcs(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        npcs = {}
        for npc_id, nd in data.items():
            npc = NPC(
                npc_id=npc_id,
                name=nd["name"],
                npc_type=nd.get("type", "simple"),
                description=nd.get("description", ""),
                dialogue=nd.get("dialogue", "")
            )
            # Загружаем инвентарь NPC из items
            for item_id in nd.get("inventory", []):
                if item_id in self.items:
                    npc.inventory.append(self.items[item_id])
            npcs[npc_id] = npc
        return npcs

    def _load_locations(self, filepath):
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
        # Используем абсолютный путь через DATA_DIR
        with open(os.path.join(DATA_DIR, "locations.json"), 'r', encoding='utf-8') as f:
            data = json.load(f)

        for loc_id, loc_data in data.items():
            current = self.locations[loc_id]

            for item_id in loc_data.get("items", []):
                if item_id in self.items:
                    current.items.append(self.items[item_id])

            for enemy_id in loc_data.get("enemies", []):
                if enemy_id in self.enemies:
                    current.enemies.append(self.enemies[enemy_id])

            for npc_id in loc_data.get("npcs", []):
                if npc_id in self.npcs:
                    current.npcs.append(self.npcs[npc_id])

            for direction, target_id in loc_data.get("exits", {}).items():
                if target_id in self.locations:
                    current.add_exit(direction, self.locations[target_id])

    def get_start_location(self, start_id="village"):
        return self.locations.get(start_id)