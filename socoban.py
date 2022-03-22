from msvcrt import getch
from copy import deepcopy
import time

BOX = 'B'
EMPTY = '.'
PLAY = '@'
BOX_PLACE = 'X'


class GameMap:
    def __init__(self, n: int):
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
        #получаем начальные координаты игрока и мест для ящиков
        for i in range(len(self.g_map)):
            for j in range(len(self.g_map)):
                if self.g_map[i][j] == PLAY:
                    self.player.append(i)
                    self.player.append(j)
                if self.g_map[i][j] == BOX_PLACE:
                    self.pl_box.append([i, j])

    # def __len__(self, g_map):
    #     return len(g_map)

    # def __getitem__(self, item):
    #     return getattr(self, item)

    #отображение игровой карты в консоли
    def view_board(self):
        print()
        for i in range(len(self.g_map)):
            for j in range(len(self.g_map)):
                print(self.g_map[i][j], end=' ')
            print()

    #проверяем победный ли ход
    def is_win(self, g_map) -> bool:
        self.box = []
        for i in range(len(g_map)):
            for j in range(len(g_map)):
                if g_map[i][j] == BOX:
                    self.box.append([i, j])
        if self.box == self.pl_box:
            return True

    #перемещение персонажа - @ стрелками
    def move(self, x: int, y: int, view: bool, *g_map: list) -> bool:
        if len(g_map) == 0:
            g_map = self.g_map
        x_old = self.player[0]
        y_old = self.player[1]
        #если перед персонажем пустое поле или поле X для ящика
        if g_map[x_old + x][y_old + y] == EMPTY or g_map[x_old + x][y_old + y] == BOX_PLACE:
            g_map[x_old + x][y_old + y] = PLAY
            if [x_old, y_old] in self.pl_box:
                g_map[x_old][y_old] = BOX_PLACE
            else:
                g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        #если перед персонажем ящик
        if g_map[x_old + x][y_old + y] == BOX and (g_map[x_old + x + x][y_old + y + y] == EMPTY
                                                        or g_map[x_old + x + x][y_old + y + y] == BOX_PLACE):
            g_map[x_old + x][y_old + y] = PLAY
            g_map[x_old + x + x][y_old + y + y] = BOX
            if [x_old, y_old] in self.pl_box:
                g_map[x_old][y_old] = BOX_PLACE
            else:
                g_map[x_old][y_old] = EMPTY
            self.player[0] = x_old + x
            self.player[1] = y_old + y
        if view:
            self.view_board()
        if self.is_win(g_map):
            return True

    #получение копии игровой карты
    def map_copy(self, g_map: list) -> list:
        c_map = deepcopy(g_map)
        return c_map

    #преобразуем ключ кнопки управления(стрелок) в пкоординаты
    def convert_coord(self, key: int) -> tuple:
        if key == 72:
            x = - 1
            y = 0
        elif key == 80:
            x = 1
            y = 0
        elif key == 75:
            x = 0
            y = - 1
        elif key == 77:
            x = 0
            y = 1
        return x, y

    #определение возможности хода в 4 направлениях
    def posible_moves(self, c_map, x: int, y: int) -> list:
        moves = []
        arrows = [72, 80, 75, 77]
        x_old = x
        y_old = y
        for arrow in arrows:
            x_new, y_new = self.convert_coord(arrow)
            if c_map[x_old + x_new][y_old + y_new] == EMPTY or (c_map[x_old + x_new][y_old + x_new] == BOX_PLACE) or \
                    (c_map[x_old + x_new][y_old + y_new] == BOX and
                     c_map[x_old + x_new + x_new][y_old + y_new + y_new] == EMPTY):
                moves.append(arrow)
        return moves

    #поиск пути для решения сокобана
    def find_solution(self, g_map):
        c_map = self.map_copy(g_map)
        moves = self.posible_moves(c_map, self.player[0], self.player[1])
        for movi in moves:
            x_new, y_new = self.convert_coord(movi)
            if self.move(x_new, y_new, c_map, False):
                print('Решение найдено!')

        pass


class Player:

    def hod(self, g_map: GameMap) -> bool:
        rez = None
        while True:
            key = ord(getch())
            if key == 80:  # стрелка вниз
                game.save_hod(80)
                rez = g_map.move(1, 0, True)
            if key == 72:  # стрелка вверх
                game.save_hod(72)
                rez = g_map.move(-1, 0, True)
            if key == 75:  # стрелка влево
                game.save_hod(75)
                rez = g_map.move(0, -1, True)
            if key == 77:  # стрелка вправо
                game.save_hod(77)
                rez = g_map.move(0, 1, True)
            if key == 27:  # ESC
                break
            if rez:
                return True


class AIPlayer:

    def hod(self, g_map: GameMap, key_ids: list) -> bool:
        rez = None
        for key in key_ids:
            time.sleep(1)
            if int(key) == 80:  # стрелка вниз
                rez = g_map.move(1, 0, True)
            if int(key) == 72:  # стрелка вверх
                rez = g_map.move(-1, 0, True)
            if int(key) == 75:  # стрелка влево
                rez = g_map.move(0, -1, True)
            if int(key) == 77:  # стрелка вправо
                rez = g_map.move(0, 1, True)
            if rez:
                return True


class Game:
    key_ids = []
    n = 0
    # запись ходов в список для повтора

    def save_hod(self, key_id: int):
        self.key_ids.append(key_id)

    #получаем карту, и запускаем AI проходить уровень по нашим записанным координатам
    def ai_replay(self):
        g_map = GameMap(self.n)
        g_map.view_board()
        pl = AIPlayer()
        pl.hod(g_map, self.key_ids)

    #replay уровня
    def replay(self):
        otv = self.valid_input_let('Хотите посмотреть replay? Введите "y" если да и "n" для выхода из игры. '
                                   'Введите ', 'y', 'n')
        if otv == 'n':
            exit()
        else:
            self.ai_replay()

    #настройки игры
    def config(self):
        print('Добро пожаловать в игру Socoban! Цель установить ящики - B, на специальные места - Х. '
              '\n Управление происходит стрелками на клавиатуре. (Выход из игры клавиша - ESC)')
        self.n = self.valid_input_dig('Выберите уровень игры: число от 1 до 5 - ')
        otv = self.valid_input_let('Хотите играть сами - выберите "y", пусть играет ИИ - выберите "n". '
                                   'Введите ', 'y', 'n')
        g_map = GameMap(self.n)
        g_map.view_board()
        if otv == 'y':
            pl = Player()
            if pl.hod(g_map):
                print('Вы победили!')
                game.replay()
        else:
            pl = AIPlayer()
            # self.key_ids = g_map.find_solution()
            # if pl.hod(g_map, self.key_ids):
            #     print('Вы победили!')


    # обработка ввода правильных буквенных ответов на диалоги
    def valid_input_let(self, text: str, zn1: str, zn2: str) -> str:
        while True:
            vvod = input(text + '"' + zn1 + '" или "' + zn2 + '": ')
            if vvod.isalpha() and (vvod == zn1 or vvod == zn2):
                return vvod
            else:
                print('Введите ' + '"' + zn1 + '" или "' + zn2 + '"!')

    #отработка корректного ввода в консоль числа(номер уровня)
    def valid_input_dig(self, text: str) -> int:
        while True:
            level = input(text)
            if level.isdigit() and int(level) >= 1 and int(level) <= 5:
                return int(level)
            else:
                print('Введите номер уровня от 1 до 5!')

if __name__ == "__main__":
    game = Game()
    game.config()
