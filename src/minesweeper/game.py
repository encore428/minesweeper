from abc import ABC
import random
import copy

from .Canvas import Canvas


def get_game_type(level, assistant):
    Gassist = assistant
    if assistant == 2:
        if level == 'beginner':
            return Beginner2()
        elif level == 'intermediate':
            return Intermediate2()
        if level == 'expert':
            return Expert2()
    elif assistant == 1:
        if level == 'beginner':
            return Beginner1()
        elif level == 'intermediate':
            return Intermediate1()
        if level == 'expert':
            return Expert1()
    else:
        if level == 'beginner':
            return Beginner0()
        elif level == 'intermediate':
            return Intermediate0()
        if level == 'expert':
            return Expert0()


class GameTracker():
    gid = 0
    # store record of game in memory
    _grid = {}

    @classmethod
    def set_grid(self, grid):

        cached_gid = self.gid
        self._grid[cached_gid] = grid
        self.gid += 1
        return cached_gid

    @classmethod
    def get_grid(self, gid):
        if gid in self._grid:
            return self._grid[gid]

        print('cannot find grid')
        # temp solution - for debugging
        game = get_game_type('beginner', 0)
        game.gen_new_game()
        self._grid[gid] = game
        return game
        # raise Exception("No grid found for key")


class Game(ABC):
    def __init__(self):
        self.reset()

    def reset(self):
        seed = 100 ## for test use fixed seed, change to none on roll out
        self._canvas = Canvas(self.width, self.height, self.initial_mines, self.assistant, seed)
        self._discovered_mines =  self._canvas.discovery
        self._no_of_remaining_tiles = self.width * self.height - self.initial_mines

    @property
    def has_won(self):
        return self._canvas.has_won

    @property
    def has_lost(self):
        return self._canvas.has_lost

    @property
    def player_board(self):
        return list(map(lambda x: x.slateSymbol[0], self._canvas.slates))

    @property
    def data(self):
        stringify_board = list(map(lambda x: x.slateSymbol[0], self._canvas.slates))
        print(stringify_board)

        return {
            "player_board": stringify_board,
            "width": self.width,
            "height": self.height,
            "assist": { 0: "Single flag",
                        1: "Dual flag",
                        2: "Intelligent"} [self._canvas.tools],
            "no_of_flags": self._canvas.cFlagCount,
            "initial_mines": self.initial_mines,
            "discovered_mines": self._discovered_mines,
            "has_won": self._canvas.hasWon,
            "has_lost": self._canvas.hasLost
        }

    def gen_new_game(self):
        self.reset()
        return self

    def reload_game(self, gid):
        self.gen_new_game()
        return {
            "gid": gid,
            **self.data
        }

    def toggle_flag(self, gid, cell_no):
        self._canvas.playFlag(int(cell_no))

        return {
            "gid": gid,
            **self.data
        }


    def open(self, gid, cell_no):
        self._canvas.playCrack(int(cell_no))
        return {
            "gid": gid,
            **self.data
        }



class Beginner0(Game):
    name = "beginner"
    height = 9
    width = 9
    initial_mines = 10
    assistant = 0


class Intermediate0(Game):
    name = "intermediate"
    height = 16
    width = 16
    initial_mines = 40
    assistant = 0


class Expert0(Game):
    name = "expert"
    height = 16
    width = 30
    initial_mines = 99
    assistant = 0

class Beginner1(Game):
    name = "beginner"
    height = 9
    width = 9
    initial_mines = 10
    assistant = 1

class Intermediate1(Game):
    name = "intermediate"
    height = 16
    width = 16
    initial_mines = 40
    assistant = 1

class Expert1(Game):
    name = "expert"
    height = 16
    width = 30
    initial_mines = 99
    assistant = 1


class Beginner2(Game):
    name = "beginner"
    height = 9
    width = 9
    initial_mines = 10
    assistant = 2

class Intermediate2(Game):
    name = "intermediate"
    height = 16
    width = 16
    initial_mines = 40
    assistant = 2

class Expert2(Game):
    name = "expert"
    height = 16
    width = 30
    initial_mines = 99
    assistant = 2
