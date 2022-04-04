"""
Game Socoban
"""
from msvcrt import getch
from copy import deepcopy
from collections import deque
import time
import sys

BOX = 'B'
BOX_ON_BOX_PLACE = '*'
EMPTY = '.'
PLAY = '@'
BOX_PLACE = 'X'
WALL = '#'
KEY_MOVES = {119: [-1, 0], 100: [0, 1], 115: [1, 0], 97: [0, -1]}
MOVES = {(-1, 0): 119, (0, 1): 100, (1, 0): 115, (0, -1): 97}
# W - 119 -> Up | D - 100  -> Right | S - 115 -> Down | A - 97 -> Left
visited = []
hashes = []


class GameMap:# pylint: disable=too-few-public-methods
    """Загрузка карты и обработка """
    def __init__(self, n_level: int):
        """Инициализация"""
        self.game_map = []
        self.n_level = n_level
        self.pl_box = []
        self.box = []
        #получаем карту из выбранного файла
        with open(f'./{n_level}.txt', 'r', encoding="utf-8") as file:
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
        """отображение игровой карты в консоли"""
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
        """проверяем победный ход или нет"""
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
        """перемещение персонажа - @ - W A S D"""
        if len(g_map) == 0:
            g_map = self.game_map
        else:
            g_map = g_map[0]

        x_old, y_old = self.get_coord_player_now(g_map)
        x_new, y_new = self.convert_key_to_coord(key)
        #если перед персонажем пустое поле или поле для ящика
        if (g_map[x_old + x_new][y_old + y_new] == EMPTY
                or g_map[x_old + x_new][y_old + y_new] == BOX_PLACE):
            g_map[x_old + x_new][y_old + y_new] = PLAY
            if [x_old, y_old] in self.pl_box:
                g_map[x_old][y_old] = BOX_PLACE
            else:
                g_map[x_old][y_old] = EMPTY
        # если перед персонажем ящик
        if ((g_map[x_old + x_new][y_old + y_new] == BOX
            or g_map[x_old + x_new][y_old + y_new] == BOX_ON_BOX_PLACE) and
                (g_map[x_old + x_new + x_new][y_old + y_new + y_new] == EMPTY
                or g_map[x_old + x_new + x_new][y_old + y_new + y_new] == BOX_PLACE)):
            g_map[x_old + x_new][y_old + y_new] = PLAY
            if g_map[x_old + x_new + x_new][y_old + y_new + y_new] == BOX_PLACE:
                g_map[x_old + x_new + x_new][y_old + y_new + y_new] = BOX_ON_BOX_PLACE
            else:
                g_map[x_old + x_new + x_new][y_old + y_new + y_new] = BOX
            g_map[x_old][y_old] = EMPTY
            if [x_old, y_old] in self.pl_box:
                g_map[x_old][y_old] = BOX_PLACE
            else:
                g_map[x_old][y_old] = EMPTY
        #выводим поле на экран если True
        if view:
            self.view_board(g_map)

    #получаем координаты игрока в данный момент
    @staticmethod
    def get_coord_player_now(game_map: list) -> tuple:
        """получаем координаты игрока в данный момент"""
        for i in range(len(game_map)):
            for j in range(len(game_map)):
                if game_map[i][j] == PLAY:
                    return i, j

    #получаем координаты ящиков в данный момент
    @staticmethod
    def get_coord_box_now(game_map: list) -> list:
        """получаем координаты ящиков в данный момент"""
        box = []
        for i in range(len(game_map)):
            for j in range(len(game_map)):
                if game_map[i][j] == BOX:
                    box.append((i, j))
        return box

    #получение копии игровой карты
    def game_map_copy(self, *game_map: list) -> list:
        """получение копии игровой карты"""
        if len(game_map) == 0:
            copy_map = deepcopy(self.game_map)
        else:
            copy_map = deepcopy(game_map[0])
        return copy_map

    #преобразуем код нажатой кнопки управления(стрелки) в координаты
    @staticmethod
    def convert_key_to_coord(key: int) -> tuple:
        """преобразуем код нажатой кнопки управления(стрелки) в координаты"""
        x_y = KEY_MOVES.get(key, 100)
        if x_y == 100:
            print('Управление происходит кнопками: W - UP, S - DOWN, A - LEFT, D - RIGHT.')
            x_coord = 0
            y_coord = 0
        else:
            x_coord = x_y[0]
            y_coord = x_y[1]
        return x_coord, y_coord

    #определение возможности хода в 4 направлениях
    def possible_moves(self, x_old: int, y_old: int, copy_map: list) -> list:
        """определение возможности хода в 4 направлениях"""
        moves = []
        for arrow in list(KEY_MOVES.keys()):
            x_new, y_new = self.convert_key_to_coord(arrow)
            if copy_map[x_old + x_new][y_old + y_new] == WALL:
                continue
            if (copy_map[x_old + x_new][y_old + y_new] == BOX
                  and copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == WALL):
                continue
            if (copy_map[x_old + x_new][y_old + y_new] == BOX
                  and copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == BOX):
                continue
            if (copy_map[x_old + x_new][y_old + y_new] == BOX_ON_BOX_PLACE
                  and copy_map[x_old + x_new + x_new][y_old + y_new + y_new] == EMPTY):
                continue
            moves.append(arrow)
        return moves

    # определение соседних венршин графа
    def possible_nodes_moves(self, x_old: int, y_old: int, copy_map: list) -> list:
        """определение соседних венршин графа"""
        moves = []
        for arrow in list(KEY_MOVES.keys()):
            x_new, y_new = self.convert_key_to_coord(arrow)
            if copy_map[x_old + x_new][y_old + y_new] == WALL:
                continue
            moves.append(arrow)
        return moves

    #получаем Hash нашей карты
    @staticmethod
    def get_map_hash(game_map: list) -> int:
        """получаем Hash нашей карты"""
        game_map_tuple = ()
        for i in range(len(game_map)):
            game_map_tuple = game_map_tuple + tuple(game_map[i])
        hash_map = hash(game_map_tuple)
        return hash_map

    #определяем расположена ли стена по координатам
    @staticmethod
    def is_wall(x_coord: int, y_coord: int, game_map: list) -> bool:
        """определяем расположена ли стена по координатам"""
        if game_map[x_coord][y_coord] == WALL:
            return True

    #строим граф ходов на игровом поле для BFS
    def build_move_graph(self) -> dict:
        """строим граф ходов на игровом поле для BFS"""
        copy_map = self.game_map_copy(self.game_map)
        move_graph = {}
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
                if not self.is_wall(i, j, copy_map):
                    node = (i, j)
                    moves = self.possible_moves(i, j, copy_map)
                    move_graph[node] = moves
        return move_graph

    # строим граф вершин на игровом поле для DFS
    def build_node_graph(self) -> dict:
        """строим граф вершин на игровом поле для DFS"""
        copy_map = self.game_map_copy(self.game_map)
        node_graph = {}
        adj_node = []
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map)):
                if not self.is_wall(i, j, copy_map):
                    node = (i, j)
                    moves = self.possible_nodes_moves(i, j, copy_map)
                    for move in moves:
                        x_new, y_new = self.convert_key_to_coord(move)
                        adj_node.append((i + x_new, j + y_new))
                    node_graph[node] = adj_node
                    adj_node = []
        return node_graph

    #определяем если ли вдоль стены место для ящика Х
    def place_x_near_wall(self, x_coord: int, y_coord: int) -> bool:
        """определяем если ли вдоль стены место для ящика Х"""
        for box in self.pl_box:
            if box[0] == x_coord or box[1] == y_coord:
                return True
        return False

    #просмотр в консоли найденного решения
    @staticmethod
    def view_find_way():
        """просмотр в консоли найденного решения"""
        print('Решение найдено, хотите увидеть прохождение карты? y/n?')
        inp = input('')
        if inp == 'y':
            game.ai_replay(True)
        elif inp == 'n':
            sys.exit()

    #решаем сокобан с помощью нахождения кратчайших путей
    def use_find(self):
        """решаем сокобан с помощью нахождения кратчайших путей
        между двумя вершинами графа с помощью BFS поиска"""
        graph = self.build_node_graph()
        game_map = self.game_map_copy()
        n_box = 0
        box_coord = []
        while not self.is_win(game_map):
            way_to_boxes = []
            boxes = self.get_coord_box_now(game_map)
            x_pl, y_pl = self.get_coord_player_now(game_map)
            #определение путей до ящиков
            for box in boxes:
                way_to_boxes.append(self.shortest_path(graph, (x_pl, y_pl), box)[1:])
            #передвижения игрока к ящику
            for move_coord in way_to_boxes[0]:
                box_coord = way_to_boxes[0][-1:]
                if move_coord == box_coord[0]:
                    break
                x_pl, y_pl = self.get_coord_player_now(game_map)
                x_pl_new = move_coord[0] - x_pl
                y_pl_new = move_coord[1] - y_pl
                key = MOVES[(x_pl_new, y_pl_new)]
                self.move_player(key, False, game_map)
                game.save_hod(key)
            box_now = box_coord.pop(0)
            pl_box = tuple(self.pl_box[n_box])
            way_box_to_x = self.shortest_path(graph, box_now, pl_box)
            i = 0
            #передвижение ящика к месту Х
            while i < (len(way_box_to_x) - 1):
                x_pl, y_pl = self.get_coord_player_now(game_map)
                way_position = (way_box_to_x[i][0] - way_box_to_x[i+1][0],
                                way_box_to_x[i][1] - way_box_to_x[i+1][1])
                need_pl_position = (way_box_to_x[i][0] + way_position[0],
                                    way_box_to_x[i][1] + way_position[1])
                #если игрок на неоходимой позиции, чтобы толкнуть ящик. толкаем ящик вперед
                if need_pl_position == (x_pl, y_pl):
                    x_pl_new = way_box_to_x[i][0] - x_pl
                    y_pl_new = way_box_to_x[i][1] - y_pl
                    key = MOVES[(x_pl_new, y_pl_new)]
                    self.move_player(key, False, game_map)
                    game.save_hod(key)
                    i += 1
                else:
                    #ставим игрока в нужную позицию для толкания ящика
                    pl_detour_box = self.pl_round_box(game_map, (x_pl, y_pl), need_pl_position)
                    for key in pl_detour_box:
                        self.move_player(key, False, game_map)
                        game.save_hod(key)
                if self.is_win(game_map):
                    return True
            n_box += 1

    #перевод игрока в нужную позицию для перемещения ящика(обход ящика вокруг)
    @staticmethod
    def pl_round_box(game_map, pl_pos: tuple, need_pos: tuple) -> list:
        """перевод игрока в нужную позицию для перемещения ящика(обход ящика вокруг)"""
        #если нужная позиция  @_BOX_need_pos
        if pl_pos[0] == need_pos[0] and pl_pos[1] < need_pos[1]:
            if (game_map[pl_pos[0] + 1][pl_pos[0]] == EMPTY
                    and game_map[pl_pos[0] + 1][pl_pos[0] + 1] == EMPTY
                    and game_map[pl_pos[0] + 1][pl_pos[0] + 2] == EMPTY):
                return [115, 100, 100, 119]
            keys = [119, 100, 100, 115]
        #если нужная позиция need_pos_BOX_@
        if pl_pos[0] == need_pos[0] and pl_pos[1] > need_pos[1]:
            if (game_map[pl_pos[0] - 1][pl_pos[0]] == EMPTY
                    and game_map[pl_pos[0] - 1][pl_pos[0] - 1] == EMPTY
                    and game_map[pl_pos[0] - 1][pl_pos[0] - 2] == EMPTY):
                return [115, 97, 97, 119]
            keys = [119, 97, 97, 115]
        #если нужная позиция над ящиком а игрок под ним
        if pl_pos[0] > need_pos[0] and pl_pos[1] == need_pos[1]:
            if (game_map[pl_pos[0]][pl_pos[0] + 1] == EMPTY
                    and game_map[pl_pos[0] - 1][pl_pos[0] + 1] == EMPTY
                    and game_map[pl_pos[0] - 2][pl_pos[0] + 1] == EMPTY):
                return [100, 119, 119, 97]
            keys = [97, 119, 119, 100]
        #если нужная позиция под ящиком а игрок над ним
        if pl_pos[0] < need_pos[0] and pl_pos[1] == need_pos[1]:
            if (game_map[pl_pos[0]][pl_pos[0] + 1] == EMPTY
                    and game_map[pl_pos[0] + 1][pl_pos[0] + 1] == EMPTY
                    and game_map[pl_pos[0] + 2][pl_pos[0] + 1] == EMPTY):
                return [100, 115, 115, 97]
            keys = [97, 115, 115, 100]
        #если нужная позиция над ящиком а игрок слева от ящика
        if pl_pos[0] > need_pos[0] and pl_pos[1] < need_pos[1]:
            if game_map[pl_pos[0]][pl_pos[1] + 1] == BOX:
                keys = [119, 100]
            #если игрок под ящиком а нужная позиция справа
            if game_map[pl_pos[0] - 1][pl_pos[1]] == BOX:
                keys = [100, 119]
        # если нужная позиция под ящиком а игрок слева от ящика
        if pl_pos[0] < need_pos[0] and pl_pos[1] < need_pos[1]:
            if game_map[pl_pos[0]][pl_pos[1] + 1] == BOX:
                keys = [115, 100]
            #если игрок под ящиком а нужная позиция слева
            if game_map[pl_pos[0] - 1][pl_pos[1]] == BOX:
                keys = [97, 100]
            #если игрок над ящиком а нужная позиция справа от него
            if game_map[pl_pos[0] + 1][pl_pos[1]] == BOX:
                keys = [100, 115]
        # если нужная позиция над ящиком а игрок справа от ящика
        if pl_pos[0] > need_pos[0] and pl_pos[1] > need_pos[1]:
            if game_map[pl_pos[0]][pl_pos[1] - 1] == BOX:
                keys = [119, 97]
        # если нужная позиция под ящиком а игрок справа от ящика
        if pl_pos[0] < need_pos[0] and pl_pos[1] > need_pos[1]:
            if game_map[pl_pos[0]][pl_pos[1] - 1] == BOX:
                keys = [115, 97]
            if game_map[pl_pos[0] + 1][pl_pos[1]] == BOX:
                keys = [97, 115]
        return keys
    #поиск кратчайшего расстояния в найденных путях
    def shortest_path(self, graph, start, goal):
        """поиск кратчайшего расстояния в найденных путях"""
        way_to_box = list(self.bfs_finds(graph, start, goal))
        sorted(way_to_box, key=len)
        return way_to_box[0]

    #Поиск возможных путей от точки start до goal в графе - поиск DFS
    @staticmethod
    def dfs_finds(graph, start, goal):
        """Поиск возможных путей от точки start до goal в графе - поиск DFS"""
        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop()
            for next_node in set(graph[vertex]) - set(path):
                if next_node == goal:
                    return path + [next_node]
                stack.append((next_node, path + [next_node]))

    # Поиск возможных путей от точки start до goal в графе - поиск BFS
    @staticmethod
    def bfs_finds(graph, start, goal):
        """Поиск возможных путей от точки start до goal в графе - поиск BFS"""
        queue = deque([(start, [start])])
        while queue:
            (vertex, path) = queue.pop()
            for next_node in set(graph[vertex]) - set(path):
                if next_node == goal:
                    yield path + [next_node]
                else:
                    queue.appendleft((next_node, path + [next_node]))

    #поиск решения методом BFS
    def bsf_find(self, *maps) -> bool:
        """поиск решения методом BFS"""
        if len(maps) == 0:
            game_map = self.game_map
        else:
            game_map = maps[0]

        copy_map = self.game_map_copy(game_map)
        x_pl, y_pl = self.get_coord_player_now(copy_map)

        pos_move = self.possible_moves(x_pl, y_pl, copy_map)
        for move in pos_move:
            copy2_map = self.game_map_copy(copy_map)
            x_move = KEY_MOVES[move][0]
            y_move = KEY_MOVES[move][1]
            if (copy2_map[x_pl + x_move][y_pl + y_move] == WALL
                    or copy2_map[x_pl + x_move][y_pl + y_move] == BOX_ON_BOX_PLACE):
                continue
            if (copy2_map[x_pl][y_pl] == BOX
                    and copy2_map[x_pl + x_move][y_pl + y_move] == EMPTY
                    and copy2_map[x_pl + x_move + x_move][y_pl + y_move + y_move] == WALL):
                continue
            if (copy2_map[x_pl + x_move][y_pl + y_move] == BOX
                    and copy2_map[x_pl + x_move * 3][y_pl + y_move * 3] == BOX):
                continue
            self.move_player(move, False, copy2_map)
            map_hash = self.get_map_hash(copy2_map)
            if map_hash not in hashes:
                if (copy2_map[x_pl + x_move][y_pl + y_move] == WALL
                        or copy2_map[x_pl + x_move][y_pl + y_move] == BOX_ON_BOX_PLACE):
                    continue
                if (copy2_map[x_pl][y_pl] == BOX
                        and copy2_map[x_pl + x_move][y_pl + y_move] == EMPTY
                        and copy2_map[x_pl + x_move + x_move][y_pl + y_move + y_move] == WALL):
                    continue
                if (copy2_map[x_pl + x_move][y_pl + y_move] == BOX
                        and copy2_map[x_pl + x_move * 3][y_pl + y_move * 3] == BOX):
                    continue
                visited.append(move)
                hashes.append(map_hash)
                self.move_player(move, True, copy_map)
                if self.is_win(copy_map):
                    self.view_find_way()
                    return True
            self.bsf_find(copy_map)


class Player: # pylint: disable=too-few-public-methods
    """Класс игрока человека"""
    #ход игрока человека
    @staticmethod
    def hod(game_map: GameMap):
        """ход игрока человека"""
        while True:
            key = ord(getch())
            if key == 27:  # ESC
                break
            game_map.move_player(key, True)
            game.save_hod(key)
            if game_map.is_win():
                return True


class AIPlayer:# pylint: disable=too-few-public-methods
    """Класс игрока человека"""
    #ход игрока АИ
    @staticmethod
    def hod(game_map: GameMap, key_ids: list, vib: bool) -> bool:
        """ход игрока АИ"""
        #если смотрим повтор прохождения уровня игрока
        if not vib:
            for key in key_ids:
                time.sleep(0.5)
                game_map.move_player(int(key), True)
                if game_map.is_win():
                    return True
        #если АИ нашел решение и просматриваем его
        while len(visited) != 0:
            time.sleep(0.5)
            key = visited.pop(0)
            game_map.move_player(key, True)
        sys.exit()


class Game:
    """Класс Игры"""
    key_ids = []
    n_level = 0

    # запись ходов в список для replay уровня
    def save_hod(self, key_id: int):
        """запись ходов в список для replay уровня"""
        self.key_ids.append(key_id)

    #получаем карту, и запускаем AI проходить уровень по нашим сохраненным координатам
    def ai_replay(self, *vib):
        """получаем карту, и запускаем AI проходить уровень по нашим сохраненным координатам"""
        if len(vib) == 0:
            key = self.key_ids
            temp = False
        else:
            key = visited
            temp = True
        game_map = GameMap(self.n_level)
        plr = AIPlayer()
        plr.hod(game_map, key, temp)

    #replay уровня
    def replay(self):
        """replay уровня"""
        otv = self._valid_input_let('Хотите посмотреть replay? Введите "y" если да '
                                   'и "n" для выхода из игры. '
                                   'Введите ', 'y', 'n')
        if otv == 'n':
            sys.exit()
        self.ai_replay()

    #настройки игры
    def config(self):
        """настройки игры"""
        print('Добро пожаловать в игру Socoban! Цель установить ящики - B,'
              ' на специальные места - Х. '
              '\n Управление происходит стрелками на клавиатуре.'
              ' (Выход из игры клавиша - ESC)')
        self.n_level = self._valid_input_dig('Выберите уровень игры: число от 1 до 5 - ')
        otv = self._valid_input_let('Хотите играть сами - выберите "y", пусть '
                                   'играет ИИ - выберите "n". '
                                   'Введите ', 'y', 'n')
        game_map = GameMap(self.n_level)
        game_map.view_board()
        if otv == 'y':
            plr = Player()
            if plr.hod(game_map):
                print('Вы победили!')
                self.replay()
        else:
            if game_map.use_find():
                otv = self._valid_input_let('Решение найдено, желаете посмотреть? y/n ', 'y', 'n')
                if otv == 'y':
                    self.ai_replay()
                sys.exit()

    # обработка ввода правильных буквенных ответов на диалоги
    @staticmethod
    def _valid_input_let(text: str, zn1: str, zn2: str) -> str:
        """обработка ввода правильных буквенных ответов на диалоги"""
        while True:
            enter = input(text + '"' + zn1 + '" или "' + zn2 + '": ')
            if enter.isalpha() and enter in (zn1, zn2):
                return enter
            print('Введите ' + '"' + zn1 + '" или "' + zn2 + '"!')

    #отработка корректного ввода в консоль числа(номер уровня)
    @staticmethod
    def _valid_input_dig(text: str) -> int:
        """отработка корректного ввода в консоль числа(номер уровня)"""
        while True:
            level = input(text)
            if level.isdigit() and (int(level) >= 1) and (int(level) <= 5):
                return int(level)
            print('Введите номер уровня от 1 до 5!')

if __name__ == "__main__":
    game = Game()
    game.config()
