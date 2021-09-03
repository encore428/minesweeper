
game_symbols = {
    'bomb': '*',
    'flag': 'f',
    'blank': 'o',
    'error_flag': 'xf',
    'empty': '-'
}


class Tile:
    def __init__(self, index):
        self._index = index
        self.__neighbours = []
        self.__surrounding_bomb_count = None
        self.__type = game_symbols['empty']

    @property
    def index(self):
        return self._index

    @property
    def neighbours(self):
        return self.__neighbours

    @property
    def surrounding_bomb_count(self):
        return self.__surrounding_bomb_count

    @surrounding_bomb_count.setter
    def surrounding_bomb_count(self, value):
        self.__surrounding_bomb_count = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def is_blank(self):
        return self.type == game_symbols['blank']

    @property
    def is_flagged(self):
        return self.type == game_symbols['flag']

    @property
    def is_a_mine(self):
        return self.type == game_symbols['bomb']

    @property
    def is_empty(self):
        return self.type == game_symbols['empty']

    def add_neighbors(self, neighbor):
        if len(neighbor) == 0:
            return

        self.__neighbours.extend(neighbor)

    def plant_mine(self):
        if not self.is_a_mine:
            self.type = game_symbols['bomb']
            self.surrounding_bomb_count = None
        else:
            raise Exception('Planting mine on existing mine')

    def increment_bomb_count(self):
        if self.is_a_mine:
            return

        if not self.surrounding_bomb_count:
            self.surrounding_bomb_count = 1
        else:
            self.surrounding_bomb_count += 1

    def toggle_flag(self):
        if self.is_blank:
            return None

        end_state = game_symbols['flag'] if self.type == game_symbols['empty'] else game_symbols['empty']
        self.type = end_state

        return end_state == game_symbols['flag']

    def set_error_flag(self):
        self.type = game_symbols['error_flag']

    def open(self):
        if self.is_blank:
            return None

        if self.surrounding_bomb_count:
            self.type = f'{self.surrounding_bomb_count}'
        elif self.is_empty:
            self.type = game_symbols['blank']

        return self.type

    def __str__(self):
        return self.type
