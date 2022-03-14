from msvcrt import getch

class Game_map():
    def __init__(self, n):
        self.g_map = []
        self.n = n
        self.player = []
        self.pl_box = []
        #получаем карту из выбранного файла
        with open(f'./{n}.txt', 'r') as file:
            for line in file:
                s_line = list(line)
                self.g_map.append(s_line[:-1])

    #отображение игровой карты в консоли
    def viev_board(self):
        print()
        for i in range(len(self.g_map)):
            for j in range(len(self.g_map)):
                print(self.g_map[i][j], end=' ')
            print()

    #поиск координат игрока и мест для ящиков
    def find_coord(self):
        for i in range(len(self.g_map)):
            for j in range(len(self.g_map)):
                if self.g_map[i][j] == '@':
                    self.player.append(i)
                    self.player.append(j)
                if self.g_map[i][j] == 'X':
                    self.pl_box.append([i, j])


    #перемещение грузчика @ стрелками
    def move(self, x, y):
        x_old = self.player[0]
        y_old = self.player[1]
        if self.g_map[x_old + x][y_old + y] == '.':
            self.g_map[x_old + x][y_old + y] = '@'
            self.g_map[x_old][y_old] = '.'
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        self.viev_board()

class Player():
    pass

class Game():

    #настройки игры
    def config(self):
        n = self.valid_input_dig('Выберите уровень игры: число от 1 до 5 - ')
        g_map = Game_map(n)
        g_map.viev_board()
        g_map.find_coord()
        game.start(g_map)

    #отработка корректного ввода в консоль числа(номер уровня)
    def valid_input_dig(self, text):
        while True:
            level = input(text)
            if level.isdigit() and int(level) >= 1 and int(level) <= 5:
                return int(level)
            else:
                print('Введите номер уровня от 1 до 5!')

    def start(self, g_map):
        while True:
            key = ord(getch())
            if key == 80:#стрелка вниз
                g_map.move(1, 0)
            if key == 72:#стрелка вверх
                g_map.move(-1, 0)
            if key == 75:#стрелка влево
                g_map.move(0, -1)
            if key == 77:#стрелка вправо
                g_map.move(0, 1)
            if key == 27:#ESC
                break



if __name__ == "__main__":
    game = Game()
    game.config()
