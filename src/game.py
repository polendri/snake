import random
import time

class Config:
    def __init__(self, arena_size, orb_count, tick_rate):
        self.arena_size = arena_size
        self.orb_count = orb_count
        self.tick_rate = tick_rate

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
        self.game_over = False
        self.exit = False

    def spawn_orb(self):
        x_pos = random.randint(0, self.config.arena_size[0] - 1)
        y_pos = random.randint(0, self.config.arena_size[1] - 1)
        self.arena[x_pos][y_pos] = Tiles.ORB

    def try_move_player(self):
        player = self.player
        if player.direction == 'U':
            next_position = (player.position[0], player.position[1] - 1)
        elif player.direction == 'D':
            next_position = (player.position[0], player.position[1] + 1)
        elif player.direction == 'L':
            next_position = (player.position[0] - 1, player.position[1])
        elif player.direction == 'R':
            next_position = (player.position[0] + 1, player.position[1])

        if self.__is_valid_position(next_position):
            self.player.position = next_position
        else:
            self.game_over = True

    def __is_valid_position(self, position):
        # Check for out-of-bounds
        if (position[0] < 0
                or position[0] >= self.config.arena_size[0]
                or position[1] < 0
                or position[1] >= self.config.arena_size[1]):
            return False

        return True

class Input:
    def __init__(self, action, key_pressed):
        self.action = action
        self.key_pressed = key_pressed

class Game:
    def __init__(self, config, display, input_source):
        self.config = config
        self.display = display
        self.input_source = input_source
        self.state = State(config)
        for _ in range(0, 3):
            self.state.spawn_orb()

    def __process_input(self, input_):
        if self.state.game_over:
            if input_.key_pressed:
                self.state.exit = True
        else:
            if input_.action == 'PLAYER_UP':
                self.state.player.direction = 'U'
            elif input_.action == 'PLAYER_DOWN':
                self.state.player.direction = 'D'
            elif input_.action == 'PLAYER_LEFT':
                self.state.player.direction = 'L'
            elif input_.action == 'PLAYER_RIGHT':
                self.state.player.direction = 'R'

    def __update(self, input_):
        self.__process_input(input_)

        if not self.state.game_over:
            self.state.try_move_player()

        self.display.draw(self.state)

    def run(self):
        tick_duration = 1 / self.config.tick_rate
        last_tick_time = time.time()

        while True:
            input_ = self.input_source.get_input()
            self.__update(input_)

            if self.state.exit:
                break

            current_time = time.time()
            sleep_time = tick_duration - (current_time - last_tick_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            last_tick_time = current_time
