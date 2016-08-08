import curses
from game import Tile

class CursesDisplay:
    """Displays the snake game in a curses window."""
    def __init__(self, stdscr, config):
        """Creates a new CursesDisplay.

        stdscr: A curses main window object, as obtained from curses.wrapper() or curses.iniscr()
        config: The game configuration settings
        """
        # Make the cursor invisible
        curses.curs_set(0)
        # Make input non-blocking
        stdscr.nodelay(True)

        margin_x = (curses.COLS - config.arena_size[0] - 2) // 2
        margin_y = (curses.LINES - config.arena_size[1] - 2) // 2

        self.stdscr = stdscr
        self.config = config
        self.arena_win = curses.newwin(
            config.arena_size[1] + 2,
            config.arena_size[0] + 2,
            max(3, margin_y),
            max(0, margin_x))
        self.message_win = curses.newwin(
            1,
            curses.COLS,
            max(margin_y + config.arena_size[1] + 1, (margin_y * 3 // 2) + config.arena_size[1]),
            0)

        self.__draw_title()
        self.stdscr.refresh()

    def __draw_title(self):
        """Draws the game title above the game arena."""
        title = 'SNAAAAKE'
        x_offset = (curses.COLS - len(title)) // 2
        y_offset = max(1, (curses.LINES - self.config.arena_size[1] - 2) // 4)
        self.stdscr.addstr(y_offset, x_offset, title)

    def __draw_tiles(self, state):
        """Draws the arena tiles (tail segments, orbs etc) to the screen."""
        tile_to_display_char = {
            Tile.EMPTY: ' ',
            Tile.ORB: 'o',
            Tile.TAIL: curses.ACS_BLOCK,
        }

        for y in range(0, self.config.arena_size[1]):
            for x in range(0, self.config.arena_size[0]):
                tile = state.arena[x][y]
                display_char = tile_to_display_char[tile]
                try:
                    self.arena_win.addch(y + 1, x + 1, display_char)
                except (curses.error):
                    # addch() fails at the bottom-right character because it tries
                    # to scroll to a new line but no line exists. Best workaround
                    # I could find.
                    # https://stackoverflow.com/questions/37648557/curses-error-add-wch-returned-an-error
                    pass

    def __draw_player(self, state):
        """Draws the player to the screen."""
        self.arena_win.addch(state.player.position[1] + 1, state.player.position[0] + 1, '@')

    def __draw_message(self, message):
        """Draws the specified one-line message to the screen below the game arena."""
        x_offset = (curses.COLS - len(message)) // 2
        self.message_win.addstr(0, x_offset, message)

    def draw(self, state):
        """Draws the screen based on the specified game state."""
        self.__draw_tiles(state)
        self.__draw_player(state)

        if state.game_over:
            self.__draw_message('Game Over! Press any key to exit. Final score: {}'.format(state.player.length))
        else:
            self.__draw_message('Score: {}'.format(state.player.length))

        self.arena_win.box()
        self.arena_win.refresh()
        self.message_win.refresh()
