import random

class Config:
    def __init__(self, arena_size=(80, 40)):
        self.arena_size = arena_size

class Tiles:
    EMPTY = ' '
    ORB = 'o'
    PLAYER_TAIL = 'X'

class Player:
    def __init__(self, position):
        self.position = position
        self.direction = 'U'
        self.length = 0

class State:
    def __init__(self, config):
        self.config = config
        self.arena = [[Tiles.EMPTY for y in range(0, config.arena_size[1])] for x in range(0, config.arena_size[0])]
        self.player = Player((config.arena_size[0] // 2, config.arena_size[1] // 2))

    def spawn_orb(self):
        x_pos = random.randint(0, self.config.arena_size[0] - 1)
        y_pos = random.randint(0, self.config.arena_size[1] - 1)
        self.arena[x_pos][y_pos] = Tiles.ORB
