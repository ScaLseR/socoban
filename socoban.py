

class Game_map():
    def __init__(self, n):
        self.g_map = []
        self.n = n
        with open(f'./{n}.txt', 'r') as file:
            for line in file:
                s_line = list(line)
                self.g_map.append(s_line[:-1])

    #отображение игровой карты в консоли
    def viev_board(self):
        for i in range(len(self.g_map)):
            for j in range(len(self.g_map)):
                print(self.g_map[i][j], end=' ')
            print()

class Player():
    pass

class Game():
    def config(self):
        n = self.valid_input_dig('Выберите уровень игры: число от 1 до 5 - ')
        g_map = Game_map(n)
        g_map.viev_board()

    #отработка корректного ввода в консоль числа(номер уровня)
    def valid_input_dig(self, text):
        while True:
            vvod = input(text)
            if vvod.isdigit() and int(vvod) >= 1 and int(vvod) <= 5:
                return int(vvod)
            else:
                print('Введите номер уровня от 1 до 5!')

if __name__ == "__main__":
    game = Game()
    game.config()