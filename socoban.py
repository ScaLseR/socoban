from msvcrt import getch
from copy import deepcopy
from pythonds.graphs import Graph
import pythonds
import time

BOX = 'B'
EMPTY = '.'
PLAY = '@'
BOX_PLACE = 'X'
WALL = '#'

class GameMap:
    def __init__(self, n: int):
        self.game_map = []
        self.n = n
        self.player = []
        self.pl_box = []
        self.box = []
        #получаем карту из выбранного файла
        with open(f'./{n}.txt', 'r') as file:
            for line in file:
                s_line = list(line)
                self.game_map.append(s_line[:-1])
        #получаем начальные координаты игрока и мест для ящиков
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
                if self.game_map[i][j] == PLAY:
                    self.player.append(i)
                    self.player.append(j)
                if self.game_map[i][j] == BOX_PLACE:
                    self.pl_box.append([i, j])

    #отображение игровой карты в консоли
    def view_board(self, *g_map: list):
        if len(g_map) == 0:
            g_map = self.game_map
        else:
            g_map = g_map[0]
        print()
        for i in range(len(g_map)):
            for j in range(len(g_map)):
                print(g_map[i][j], end=' ')
            print()

    #проверяем победный ли ход
    def is_win(self, *game_map: list) -> bool:
        if len(game_map) == 0:
            game_map = self.game_map
        else:
            game_map = game_map[0]
        self.box = []
        for i in range(len(game_map)):
            for j in range(len(game_map)):
                if game_map[i][j] == BOX:
                    self.box.append([i, j])
        if self.box == self.pl_box:
            return True

    #перемещение персонажа - @ стрелками
    def move(self, x: int, y: int, view: bool, *g_map: list):
        if len(g_map) == 0:
            g_map = self.game_map
        else:
            g_map = g_map[0]
        x_old, y_old = self.get_coord_player(g_map)
        #self.view_board(g_map)
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
            self.view_board(g_map)

    #получаем координаты игрока в данный момент
    def get_coord_player(self, game_map: list) -> tuple:
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
                if game_map[i][j] == PLAY:
                    return i, j

    #получение копии игровой карты
    def game_map_copy(self, *game_map: list) -> list:
        if len(game_map) == 0:
            game_map = self.game_map
        copy_map = deepcopy(game_map[0])
        return copy_map

    #преобразуем код нажатой кнопки управления(стрелки) в координаты
    def convert_key_to_coord(self, key: int) -> tuple:
        x = 0
        y = 0
        if key == 72:
            x -= 1
        elif key == 80:
            x += 1
        elif key == 75:
            y -= 1
        elif key == 77:
            y += 1
        return x, y

    #определение возможности хода в 4 направлениях
    def possible_moves(self, x_old: int, y_old: int, copy_map: list) -> list:
        moves = []
        arrows = [72, 80, 75, 77]
        for arrow in arrows:
            x_new, y_new = self.convert_key_to_coord(arrow)
            if (copy_map[x_old + x_new][y_old + y_new] == WALL) or \
                    ((copy_map[x_old + x_new][y_old + y_new] == BOX) and
                    (copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == WALL)) or\
                    ((copy_map[x_old + x_new][y_old + y_new] == BOX) and
                     (copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == BOX)):
                continue
            else:
                moves.append([x_new, y_new])
        return moves

    #получаем Hash нашей карты
    def get_map_hash(self, game_map: list) -> int:
        game_map_tuple = ()
        for i in range(len(game_map)):
            game_map_tuple = game_map_tuple + tuple(game_map[i])
        hash_map = hash(game_map_tuple)
        return hash_map

    #определяем расположена ли стена по координатам
    def is_wall(self, x: int, y: int, game_map: list) -> bool:
        if game_map[x][y] == WALL:
            return True

    #строим граф ходов на игровом поле
    def build_move_graph(self):
        copy_map = self.game_map_copy(self.game_map)
        muve_graph = {}
        adj_node = []
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
                if not self.is_wall(i, j, copy_map):
                    node = (i, j)
                    moves = self.possible_moves(i, j, copy_map)
                    for move in moves:
                        adj_node.append([i + move[0], j + move[1]])
                    muve_graph[node] = adj_node
                    adj_node = []
        print(muve_graph)

    #поиск пути для решения сокобана
    # def find_solution(self, *game_map: list):
    #     queue = []
    #     hashes = []
    #     gr = {}
    #     if len(game_map) == 0:
    #         game_map = self.game_map
    #     else:
    #         game_map = game_map[0]
    #
    #     copy_map = self.game_map_copy(game_map)
    #     hashes.append(self.get_hash(copy_map))
    #     x_pl, y_pl = self.get_coord_player(copy_map)
    #     queue.append([x_pl, y_pl])
    #
    #     while queue:
    #         first = queue.pop(0)
    #         print()
    #         x_pl, y_pl = self.get_coord_player(copy_map)
    #         self.move(first[0] - x_pl, first[0] - y_pl, True, copy_map)
    #         moves = self.possible_moves(first[0], first[1], copy_map)
    #         list_coord = []
    #         print('moves= ', moves)
    #         for move in moves:
    #             temp_copy_map = self.game_map_copy(copy_map)
    #             coord_mov = [first[0] + move[0], first[1] + move[1]]
    #             self.move(move[0], move[1], False, temp_copy_map)
    #             temp_hash = self.get_hash(temp_copy_map)
    #             queue.append(coord_mov)
    #             hashes.append(temp_hash)
    #             list_coord.append([move[0], move[1]])
    #             #x_pl, y_pl = self.get_coord_player(temp_copy_map)
    #             #self.move(first[0] - x_pl, first[0] - y_pl, True, copy_map)
    #         gr[(first[0], first[1])] = list_coord
    #         print(gr)


class Player:

    def hod(self, game_map: GameMap):
        while True:
            key = ord(getch())
            if key == 27:  # ESC
                break
            x, y = game_map.convert_key_to_coord(key)
            game_map.move(x, y, True)
            game.save_hod(key)
            if game_map.is_win():
                return True


class AIPlayer:

    def hod(self, game_map: GameMap, key_ids: list):
        for key in key_ids:
            time.sleep(0.5)
            x, y = game_map.convert_key_to_coord(int(key))
            game_map.move(x, y, True)
            if game_map.is_win():
                return True


class Game:
    key_ids = []
    n = 0

    # запись ходов в список для повтора
    def save_hod(self, key_id: int):
        self.key_ids.append(key_id)

    #получаем карту, и запускаем AI проходить уровень по нашим записанным координатам
    def ai_replay(self):
        game_map = GameMap(self.n)
        pl = AIPlayer()
        pl.hod(game_map, self.key_ids)

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
        game_map = GameMap(self.n)
        game_map.view_board()
        if otv == 'y':
            pl = Player()
            if pl.hod(game_map):
                print('Вы победили!')
                game.replay()
        else:
            pl = AIPlayer()
            game_map.build_move_graph()
            #game_map.find_solution()

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
