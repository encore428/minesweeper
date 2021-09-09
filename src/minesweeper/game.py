from abc import ABC
import random
import copy

from .Canvas import Canvas


def get_game_type(level, assistant):
    myGame = JustGame()
    myGame.name = level
    myGame.assistant = assistant
    if level == 'intermediate':
        myGame.height = 16
        myGame.width = 16
        myGame.initial_mines = 40
    if level == 'expert':
        myGame.height = 16
        myGame.width = 30
        myGame.initial_mines = 99
    return myGame


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
        seed = None ## for test use fixed seed, change to none on roll out
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


class JustGame(Game):
    name = "beginner"
    height = 9
    width = 9
    initial_mines = 10
    assistant = 0
