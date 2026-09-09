class Location:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.exits = {}          # словарь: направление -> Location
        self.items = []          # предметы на земле
        self.enemies = []        # враги, которые могут встретиться

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
        if self.exits:
            print("Выходы:", ", ".join(self.exits.keys()))