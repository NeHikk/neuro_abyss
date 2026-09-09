class Item:
    def __init__(self, name, item_type, description="", effect=0):
        self.name = name
        self.type = item_type   # weapon, armor, heal, energy, stability, craft
        self.description = description
        self.effect = effect    # для оружия – урон, для аптечки – лечение и т.д.

    def __str__(self):
        return self.name