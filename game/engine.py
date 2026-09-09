class Game:
    def __init__(self):
        self.running = True

    def run(self):
        print("=== НейроБездна ===")
        print("Ты просыпаешься в разрушенном комплексе. Нейросфера мертва, но её эхо ещё звучит.")
        while self.running:
            cmd = input("> ").strip().lower()
            if cmd in ("выход", "exit", "quit"):
                self.running = False
                print("Игра завершена.")
            elif cmd in ("помощь", "help"):
                print("Команды: осмотреться, статус, выход")
            elif cmd == "осмотреться":
                print("Вокруг обломки серверов и мигающие огни.")
            elif cmd == "статус":
                print("Здоровье: 100, Энергия: 50, Стабильность: 0")
            else:
                print("Неизвестная команда.")