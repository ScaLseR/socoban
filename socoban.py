from msvcrt import getch
from copy import deepcopy
from collections import deque
import time

BOX = 'B'
BOX_ON_BOX_PLACE = '*'
EMPTY = '.'
PLAY = '@'
PLAY_ON_BOX_PLACE = '$'
BOX_PLACE = 'X'
WALL = '#'
KEY_MOVES = {119: [-1, 0], 100: [0, 1], 115: [1, 0], 97: [0, -1]}
# W - 119 -> Up | D - 100  -> Right | S - 115 -> Down | A - 97 -> Left


class GameMap:
    def __init__(self, n: int):
        self.game_map = []
        self.n = n
        self.pl_box = []
        self.box = []
        #получаем карту из выбранного файла
        with open(f'./{n}.txt', 'r') as file:
            for line in file:
                s_line = list(line)
                self.game_map.append(s_line[:-1])
        #получаем начальные координаты мест для ящиков
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
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

    #проверяем победный ход или нет
    def is_win(self, *game_map: list) -> bool:
        if len(game_map) == 0:
            game_map = self.game_map
        else:
            game_map = game_map[0]
        self.box = []
        for i in range(len(game_map)):
            for j in range(len(game_map)):
                if game_map[i][j] == BOX_ON_BOX_PLACE:
                    self.box.append([i, j])
        if self.box == self.pl_box:
            return True

    #перемещение персонажа - @ - W A S D
    def move_player(self, key: int, view: bool, *g_map: list):
        if len(g_map) == 0:
            g_map = self.game_map
        else:
            g_map = g_map[0]

        x_old, y_old = self.get_coord_player_now(g_map)
        x, y = self.convert_key_to_coord(key)
        #если перед персонажем пустое поле и он не стоит на месте для ящика
        if g_map[x_old + x][y_old + y] == EMPTY and g_map[x_old][y_old] == PLAY:
            g_map[x_old + x][y_old + y] = PLAY
            g_map[x_old][y_old] = EMPTY
        #если перед персонажем поле X для ящика
        if g_map[x_old + x][y_old + y] == BOX_PLACE:
            g_map[x_old + x][y_old + y] = PLAY_ON_BOX_PLACE
            g_map[x_old][y_old] = EMPTY
        #если перед персонажем пустое поле и он стоит на месте для ящика
        if g_map[x_old + x][y_old + y] == EMPTY and g_map[x_old][y_old] == PLAY_ON_BOX_PLACE:
            g_map[x_old + x][y_old + y] = PLAY
            g_map[x_old][y_old] = BOX_PLACE
        #если перед персонажем ящик и перед ящиком пустое поле
        if g_map[x_old][y_old] == PLAY and g_map[x_old + x][y_old + y] == BOX and g_map[x_old + x + x]\
                [y_old + y + y] == EMPTY:
            g_map[x_old + x][y_old + y] = PLAY
            g_map[x_old + x + x][y_old + y + y] = BOX
            g_map[x_old][y_old] = EMPTY
        #если перед персонажем ящик и перед ящиком место для ящика
        if g_map[x_old + x][y_old + y] == BOX and g_map[x_old + x + x][y_old + y + y] == BOX_PLACE:
            g_map[x_old + x][y_old + y] = PLAY
            g_map[x_old + x + x][y_old + y + y] = BOX_ON_BOX_PLACE
            g_map[x_old][y_old] = EMPTY
        #если ящик стоит на месте и впереди пустое поле
        if g_map[x_old + x][y_old + y] == BOX_ON_BOX_PLACE and g_map[x_old + x + x][y_old + y + y] == EMPTY:
            g_map[x_old + x][y_old + y] = PLAY_ON_BOX_PLACE
            g_map[x_old + x + x][y_old + y + y] = BOX
            g_map[x_old][y_old] = EMPTY
        #если персонаж стоит на месте для ящика, впереди ящик и пустое поле
        if g_map[x_old][y_old] == PLAY_ON_BOX_PLACE and g_map[x_old + x][y_old + y] == BOX and g_map[x_old + x + x]\
                [y_old + y + y] == EMPTY:
            g_map[x_old + x][y_old + y] = PLAY
            g_map[x_old + x + x][y_old + y + y] = BOX
            g_map[x_old][y_old] = BOX_PLACE
        #выводим поле на экран если True
        if view:
            self.view_board(g_map)

    #получаем координаты игрока в данный момент
    @staticmethod
    def get_coord_player_now(game_map: list) -> tuple:
        for i in range(len(game_map)):
            for j in range(len(game_map)):
                if game_map[i][j] == PLAY or game_map[i][j] == PLAY_ON_BOX_PLACE:
                    return i, j

    #получение копии игровой карты
    def game_map_copy(self, *game_map: list) -> list:
        if len(game_map) == 0:
            game_map = self.game_map
        copy_map = deepcopy(game_map[0])
        return copy_map

    #преобразуем код нажатой кнопки управления(стрелки) в координаты
    @staticmethod
    def convert_key_to_coord(key: int) -> tuple:
        x_y = KEY_MOVES.get(key, 100)
        if x_y == 100:
            print('Управление происходит кнопками: W - UP, S - DOWN, A - LEFT, D - RIGHT.')
            x = 0
            y = 0
        else:
            x = x_y[0]
            y = x_y[1]
        return x, y

    #определение возможности хода в 4 направлениях
    def possible_moves(self, x_old: int, y_old: int, copy_map: list) -> list:
        moves = []
        for arrow in list(KEY_MOVES.keys()):
            x_new, y_new = self.convert_key_to_coord(arrow)
            if (copy_map[x_old + x_new][y_old + y_new] == WALL) or \
                    ((copy_map[x_old + x_new][y_old + y_new] == BOX) and
                     (copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == WALL)) or \
                    ((copy_map[x_old + x_new][y_old + y_new] == BOX) and
                     (copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == BOX)):
                continue
            else:
                moves.append(arrow)
        return moves

    #получаем Hash нашей карты
    @staticmethod
    def get_map_hash(game_map: list) -> int:
        game_map_tuple = ()
        for i in range(len(game_map)):
            game_map_tuple = game_map_tuple + tuple(game_map[i])
        hash_map = hash(game_map_tuple)
        return hash_map

    #определяем расположена ли стена по координатам
    @staticmethod
    def is_wall(x: int, y: int, game_map: list) -> bool:
        if game_map[x][y] == WALL:
            return True

    #строим граф ходов на игровом поле
    def build_move_graph(self) -> dict:
        copy_map = self.game_map_copy(self.game_map)
        move_graph = {}
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
                if not self.is_wall(i, j, copy_map):
                    node = (i, j)
                    moves = self.possible_moves(i, j, copy_map)
                    move_graph[node] = moves
        return move_graph

    def get_list_coord_box_player_walls(self):
        box_player = []
        wall_storage = []
        n = len(self.game_map)

        for i in range(n):
            box_player.append([])
            wall_storage.append([])
            for j in range(n):
                box_player[-1].append('-')
                wall_storage[-1].append('-')

        for i in range(n):
            for j in range(n):
                if self.game_map[i][j] == 'B' or self.game_map[i][j] == 'R':
                    box_player[i][j] = self.game_map[i][j]
                    wall_storage[i][j] = ' '
                elif self.game_map[i][j] == 'S' or self.game_map[i][j] == 'O':
                    wall_storage[i][j] = self.game_map[i][j]
                    box_player[i][j] = ' '
                elif self.game_map[i][j] == ' ':
                    box_player[i][j] = ' '
                    wall_storage[i][j] = ' '
                elif self.game_map[i][j] == '*':
                    box_player[i][j] = 'B'
                    wall_storage[i][j] = 'S'
                elif self.game_map[i][j] == '.':
                    box_player[i][j] = 'R'
                    wall_storage[i][j] = 'S'
        return box_player, wall_storage

    def bfs(self):
        moves_list = []
        visited_moves = []
        box_player, wall_storage = self.get_list_coord_box_player_walls()
        queue = deque([])
        source = [box_player, wall_storage]

    # def bfs(self):
    #     queue = []
    #     visited = []
    #     hashes = []
    #     graph = self.build_move_graph()
    #     copy_map = self.game_map_copy(self.game_map)
    #     x_pl, y_pl = self.get_coord_player_now(copy_map)
    #     queue.append(72)
    #     while queue:
    #         s = queue.pop(0)
    #         print('s= ', s)
    #         x_pl, y_pl = self.get_coord_player_now(copy_map)
    #         x_new = s[0] - x_pl
    #         y_new = s[1] - y_pl
    #         print('x_new= ', x_new, 'y_new= ', y_new)
    #         self.move_player(key, True, copy_map)
    #         hash = self.get_map_hash(copy_map)
    #         print('queue= ', queue)
    #         print('visited= ', visited)
    #
    #         if hash not in hashes:
    #             hashes.append(hash)
    #             print('hashes= ', hashes)
    #             visited.append(s)
    #             if self.is_win(copy_map):
    #                 print('Выйигрышная комбинация найдена!')
    #                 return s
    #             for neighbour in graph[s]:
    #                 print('neighbour= ', neighbour)
    #                 if neighbour not in visited:
    #                     queue.append(neighbour)
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

    @staticmethod
    def hod(game_map: GameMap):
        while True:
            key = ord(getch())
            if key == 27:  # ESC
                break
            game_map.move_player(key, True)
            game.save_hod(key)
            if game_map.is_win():
                return True


class AIPlayer:
    @staticmethod
    def hod(game_map: GameMap, key_ids: list):
        for key in key_ids:
            time.sleep(0.5)
            game_map.move_player(int(key), True)
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
            game_map.bfs()
            #game_map.find_solution()

    # обработка ввода правильных буквенных ответов на диалоги
    @staticmethod
    def valid_input_let(text: str, zn1: str, zn2: str) -> str:
        while True:
            enter = input(text + '"' + zn1 + '" или "' + zn2 + '": ')
            if enter.isalpha() and (enter == zn1 or enter == zn2):
                return enter
            else:
                print('Введите ' + '"' + zn1 + '" или "' + zn2 + '"!')

    #отработка корректного ввода в консоль числа(номер уровня)
    @staticmethod
    def valid_input_dig(text: str) -> int:
        while True:
            level = input(text)
            if level.isdigit() and (int(level) >= 1) and (int(level) <= 5):
                return int(level)
            else:
                print('Введите номер уровня от 1 до 5!')

if __name__ == "__main__":
    game = Game()
    game.config()
