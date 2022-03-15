from msvcrt import getch

BOX = 'B'
EMPTY = '.'
PLAY = '@'
BOX_PLACE = 'X'

class Game_map():
    def __init__(self, n):
        self.g_map = []
        self.n = n
        self.player = []
        self.pl_box = []
        self.box = []
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
                if self.g_map[i][j] == PLAY:
                    self.player.append(i)
                    self.player.append(j)
                if self.g_map[i][j] == BOX_PLACE:
                    self.pl_box.append([i, j])

    def is_win(self):
        self.box = []
        for i in range(len(self.g_map)):
            for j in range(len(self.g_map)):
                if self.g_map[i][j] == BOX:
                    self.box.append([i, j])
        if self.box == self.pl_box:
            print()
            print('******************')
            print('* Вы победили!!! *')
            print('******************')
            exit()
        print('self.box =', self.box)

    #перемещение персонажа - @ стрелками
    def move(self, x, y):
        x_old = self.player[0]
        y_old = self.player[1]
        #если перед персонажем пустое поле
        if self.g_map[x_old + x][y_old + y] == EMPTY:
            self.g_map[x_old + x][y_old + y] = PLAY
            if [x_old, y_old] in self.pl_box:
                self.g_map[x_old][y_old] = BOX_PLACE
            else:
                self.g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        # если перед персонажем поле X для ящика
        if self.g_map[x_old + x][y_old + y] == BOX_PLACE:
            self.g_map[x_old + x][y_old + y] = PLAY
            if [x_old, y_old] in self.pl_box:
                self.g_map[x_old][y_old] = BOX_PLACE
            else:
                self.g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        #если перед персонажем ящик
        if self.g_map[x_old + x][y_old + y] == BOX and (self.g_map[x_old + x + x][y_old + y + y] == EMPTY or self.g_map[x_old + x + x][y_old + y + y] == BOX_PLACE):
            self.g_map[x_old + x][y_old + y] = PLAY
            self.g_map[x_old + x + x][y_old + y + y] = BOX
            if [x_old, y_old] in self.pl_box:
                self.g_map[x_old][y_old] = BOX_PLACE
            else:
                self.g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        self.viev_board()
        self.is_win()

class Player:
    def hod(self, g_map):
        while True:
            key = ord(getch())
            if key == 80:  # стрелка вниз
                g_map.move(1, 0)
            if key == 72:  # стрелка вверх
                g_map.move(-1, 0)
            if key == 75:  # стрелка влево
                g_map.move(0, -1)
            if key == 77:  # стрелка вправо
                g_map.move(0, 1)
            if key == 27:  # ESC
                break


class Game:
    #настройки игры
    def config(self):
        print('Добро пожаловать в игру Socoban! Цель установить ящики - B, на специальные места - Х. \n Управление происходит стрелками на клавиатуре. (Выход из игры клавиша - ESC)')
        n = self.valid_input_dig('Выберите уровень игры: число от 1 до 5 - ')
        g_map = Game_map(n)
        g_map.viev_board()
        g_map.find_coord()
        pl = Player()
        pl.hod(g_map)

    #отработка корректного ввода в консоль числа(номер уровня)
    def valid_input_dig(self, text):
        while True:
            level = input(text)
            if level.isdigit() and int(level) >= 1 and int(level) <= 5:
                return int(level)
            else:
                print('Введите номер уровня от 1 до 5!')

if __name__ == "__main__":
    game = Game()
    game.config()
