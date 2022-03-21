from msvcrt import getch
import time

BOX = 'B'
EMPTY = '.'
PLAY = '@'
BOX_PLACE = 'X'


class GameMap:
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
    def view_board(self):
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
            print('\n******************')
            print('* Вы победили!!! *')
            print('******************')
            game.replay()

    #перемещение персонажа - @ стрелками
    def move(self, x, y):
        x_old = self.player[0]
        y_old = self.player[1]
        #если перед персонажем пустое поле или поле X для ящика
        if self.g_map[x_old + x][y_old + y] == EMPTY or self.g_map[x_old + x][y_old + y] == BOX_PLACE:
            self.g_map[x_old + x][y_old + y] = PLAY
            if [x_old, y_old] in self.pl_box:
                self.g_map[x_old][y_old] = BOX_PLACE
            else:
                self.g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        if self.g_map[x_old + x][y_old + y] == BOX and (self.g_map[x_old + x + x][y_old + y + y] == EMPTY
                                                        or self.g_map[x_old + x + x][y_old + y + y] == BOX_PLACE):
            self.g_map[x_old + x][y_old + y] = PLAY
            self.g_map[x_old + x + x][y_old + y + y] = BOX
            if [x_old, y_old] in self.pl_box:
                self.g_map[x_old][y_old] = BOX_PLACE
            else:
                self.g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        self.view_board()
        self.is_win()


class Player:

    def hod(self, g_map):
        while True:
            key = ord(getch())
            if key == 80:  # стрелка вниз
                game.save_hod(80)
                g_map.move(1, 0)
            if key == 72:  # стрелка вверх
                game.save_hod(72)
                g_map.move(-1, 0)
            if key == 75:  # стрелка влево
                game.save_hod(75)
                g_map.move(0, -1)
            if key == 77:  # стрелка вправо
                game.save_hod(77)
                g_map.move(0, 1)
            if key == 27:  # ESC
                break


class AIPlayer:

    def hod(self, g_map, key_ids):
        for key in key_ids:
            time.sleep(1)
            if int(key) == 80:  # стрелка вниз
                g_map.move(1, 0)
            if int(key) == 72:  # стрелка вверх
                g_map.move(-1, 0)
            if int(key) == 75:  # стрелка влево
                g_map.move(0, -1)
            if int(key) == 77:  # стрелка вправо
                g_map.move(0, 1)


class Game:
    key_ids = []
    n = 0
    # запись ходов в список для повтора

    def save_hod(self, key_id):
        self.key_ids.append(key_id)

    #получаем карту, и запускаем AI проходить уровень по нашим записанным координатам
    def ai_play(self):
        g_map = GameMap(self.n)
        g_map.view_board()
        g_map.find_coord()
        pl = AIPlayer()
        pl.hod(g_map, self.key_ids)

    #replay уровня
    def replay(self):
        otv = self.valid_input_let('Хотите посмотреть replay? Введите "y" если да и "n" для выхода из игры. '
                                   'Введите ', 'y', 'n')
        if otv == 'n':
            exit()
        else:
            self.ai_play()

    #настройки игры
    def config(self):
        print('Добро пожаловать в игру Socoban! Цель установить ящики - B, на специальные места - Х. '
              '\n Управление происходит стрелками на клавиатуре. (Выход из игры клавиша - ESC)')
        self.n = self.valid_input_dig('Выберите уровень игры: число от 1 до 5 - ')
        otv = self.valid_input_let('Хотите играть сами - выберите "y", пусть играет ИИ - выберите "n". '
                                   'Введите ', 'y', 'n')
        g_map = GameMap(self.n)
        g_map.view_board()
        g_map.find_coord()
        if otv == 'y':
            pl = Player()
            pl.hod(g_map)
        else:
            pl = AIPlayer()
            pl.hod(g_map, self.key_ids)

    # обработка ввода правильных буквенных ответов на диалоги
    def valid_input_let(self, text, zn1, zn2):
        while True:
            vvod = input(text + '"' + zn1 + '" или "' + zn2 + '": ')
            if vvod.isalpha() and (vvod == zn1 or vvod == zn2):
                return vvod
            else:
                print('Введите ' + '"' + zn1 + '" или "' + zn2 + '"!')

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
