from collections import deque
import random
import time

class Config:
    """Defines configuration options for the game."""
    def __init__(self, arena_size, orb_count, tick_rate):
        """Creates a new Config.

        arena_size: A tuple describing the width and height of the game arena
        orb_count: The number of randomly-spawned orbs which exist at a given time
        tick_rate: The number of game ticks which elapse per second
        """
        self.arena_size = arena_size
        self.orb_count = orb_count
        self.tick_rate = tick_rate

class Tile:
    EMPTY = ' '
    ORB = 'o'
    TAIL = 'X'

class Player:
    """Defines the player (snake head) and associated data."""
    def __init__(self, position):
        """Creates a new Player.

        position: A tuple describing the player's position
        direction: One of 'U', 'D', 'L', or 'R', describing the direciton the player is facing
        length: The length of the player's tail
        """
        self.position = position
        self.direction = 'U'
        self.length = 0

class Tail:
    """Defines a segment of the player tail."""
    def __init__(self, position, expiry_tick):
        """Creates a new Tail.

        position: A tuple describing the position of the tail segment
        expiry_tick: The tick number at which time this segment should disappear
        """
        self.position = position
        self.expiry_tick = expiry_tick

class State:
    """Defines the overall state of a game, and operations to mutate the state."""
    def __init__(self, config):
        """Creates a new State.

        config: The game's configuration options
        """
        self.config = config
        # 2D array describing the game arena
        self.arena = [[Tile.EMPTY for y in range(0, config.arena_size[1])] for x in range(0, config.arena_size[0])]
        self.player = Player((config.arena_size[0] // 2, config.arena_size[1] // 2))
        # Queue of tail segments
        self.tails = deque()
        # The current tick number
        self.tick = 0
        # True if the game is over
        self.game_over = False
        # True if the game should exit
        self.exit = False

    def spawn_orb(self):
        """Spawns an orb at a random location in the arena."""
        x_pos = random.randint(0, self.config.arena_size[0] - 1)
        y_pos = random.randint(0, self.config.arena_size[1] - 1)
        self.arena[x_pos][y_pos] = Tile.ORB

    def eat_orbs(self):
        """Handles "eating" orbs when the player is on top of them, increasing the player's tail length."""
        player_occupied_tile = self.arena[self.player.position[0]][self.player.position[1]]
        if player_occupied_tile == Tile.ORB:
            self.arena[self.player.position[0]][self.player.position[1]] = Tile.EMPTY
            self.player.length = self.player.length + 1
            self.spawn_orb()

    def spawn_tail(self):
        """Spawns a new tail segment at the player's current position."""
        self.arena[self.player.position[0]][self.player.position[1]] = Tile.TAIL
        self.tails.append(Tail(self.player.position, self.tick + self.player.length))

    def cut_tail(self):
        """Removes tail segments which should no longer exist."""
        while len(self.tails) > 0 and self.tails[0].expiry_tick == self.tick:
            tail = self.tails.popleft()
            self.arena[tail.position[0]][tail.position[1]] = Tile.EMPTY

    def try_move_player(self):
        """Moves the player forwards if possible, or else ends the game."""
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
        """Returns True if the specified position is valid (in bounds and unobstructed), False otherwise."""
        return (position[0] >= 0
            and position[0] < self.config.arena_size[0]
            and position[1] >= 0
            and position[1] < self.config.arena_size[1]
            and self.arena[position[0]][position[1]] != Tile.TAIL)

class Input:
    """Defines a single player input event."""
    def __init__(self, action, key_pressed):
        """Creates a new Input.

        action: A string describing the action requested
        key_pressed: True if any key was pressed, False otherwise
        """
        self.action = action
        self.key_pressed = key_pressed

class Game:
    """Manages the execution of the game."""
    def __init__(self, config, display, input_source):
        """Creates a new Game.

        config: The game Config
        display: The game Display
        input_source: The game InputSource
        """
        self.config = config
        self.display = display
        self.input_source = input_source
        self.state = State(config)
        for _ in range(0, self.config.orb_count):
            self.state.spawn_orb()

    def __process_input(self, input_):
        """Mutates state according to the specified input event."""
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
        """Advances the game state by one tick."""
        self.__process_input(input_)

        if not self.state.game_over:
            self.state.spawn_tail()
            self.state.try_move_player()
        if not self.state.game_over:
            self.state.cut_tail()
            self.state.eat_orbs()

        self.display.draw(self.state)
        self.state.tick = self.state.tick + 1

    def run(self):
        """Runs the game loop, exiting once the player has lost and pressed a key."""
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
