class Quest:
    """
    Один квест. Хранит описание, цель, награду и текущий прогресс.
    """
    def __init__(self, quest_id, data):
        self.id = quest_id
        self.name = data["name"]
        self.description = data["description"]
        self.type = data["type"]                 # collect, kill, talk
        self.target = data["target"]             # id предмета/врага/NPC
        self.amount = data.get("amount", 1)      # сколько нужно
        self.reward_items = data.get("reward_items", [])
        self.reward_reputation = data.get("reward_reputation", {})
        self.giver = data.get("giver", None)     # id NPC, который выдал

        self.progress = 0                        # текущий прогресс
        self.is_completed = False                # выполнен ли
        self.is_turned_in = False                # сдан ли NPC

    def check_completion(self):
        """Обновляет статус выполнения, если прогресс достиг цели."""
        if self.progress >= self.amount:
            self.is_completed = True

    def add_progress(self, count=1):
        """Увеличивает прогресс (например, при подборе предмета или убийстве врага)."""
        if self.is_completed:
            return
        self.progress += count
        self.check_completion()

    def show(self):
        """Красивый вывод в журнале."""
        status = "✅ выполнен" if self.is_completed else f"{self.progress}/{self.amount}"
        if self.is_turned_in:
            status = "🏁 сдан"
        print(f"  [{self.id}] {self.name} — {status}")
        print(f"     {self.description}")


class QuestLog:
    """
    Журнал квестов игрока. Хранит активные и завершённые задания.
    """
    def __init__(self):
        self.active = {}      # id -> Quest
        self.completed = {}   # id -> Quest

    def add_quest(self, quest):
        """Добавить новый квест в журнал."""
        if quest.id in self.active or quest.id in self.completed:
            print(f"Квест '{quest.name}' уже есть в журнале.")
            return False
        self.active[quest.id] = quest
        print(f"\n📜 Новый квест: {quest.name}")
        print(f"   {quest.description}")
        return True

    def has_quest(self, quest_id):
        return quest_id in self.active or quest_id in self.completed

    def progress_on(self, target_type, target_id, count=1):
        """
        Обновляет прогресс по всем активным квестам, чья цель совпадает.
        target_type: 'collect' (предмет), 'kill' (враг), 'talk' (NPC)
        """
        for quest in self.active.values():
            if quest.type == target_type and quest.target == target_id:
                quest.add_progress(count)

    def get_completed_ready(self):
        """Возвращает список квестов, готовых к сдаче (выполнены, но не сданы)."""
        return [q for q in self.active.values() if q.is_completed and not q.is_turned_in]

    def turn_in(self, quest_id):
        """Пометить квест как сданный и переместить в completed."""
        if quest_id not in self.active:
            return None
        quest = self.active.pop(quest_id)
        quest.is_turned_in = True
        self.completed[quest_id] = quest
        return quest

    def show_journal(self):
        """Показать весь журнал."""
        print("\n=== ЖУРНАЛ КВЕСТОВ ===")
        if not self.active and not self.completed:
            print("Журнал пуст.")
            return

        if self.active:
            print("\n📌 Активные:")
            for quest in self.active.values():
                quest.show()

        if self.completed:
            print("\n🏆 Завершённые:")
            for quest in self.completed.values():
                quest.show()