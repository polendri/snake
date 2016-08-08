import curses
from game import Tiles

class CursesDisplay:
    def __init__(self, stdscr, config):
        # Make the cursor invisible
        curses.curs_set(0)
        # Make input non-blocking
        stdscr.nodelay(True)
        
        margin_x = (curses.COLS - config.arena_size[0]) // 2
        margin_y = (curses.LINES - config.arena_size[1]) // 2

        self.stdscr = stdscr
        self.config = config
        self.arena_win = curses.newwin(
            config.arena_size[1],
            config.arena_size[0],
            max(4, margin_y),
            max(1, margin_x))
        self.message_win = curses.newwin(
            1,
            curses.COLS,
            max(margin_y + config.arena_size[1] + 1, (margin_y * 3 // 2) + config.arena_size[1]),
            0)

        self.__draw_title()
        self.stdscr.refresh()

    def __draw_title(self):
        title = 'SNAAAAKE'
        x_offset = (curses.COLS - len(title)) // 2
        y_offset = max(1, (curses.LINES - self.config.arena_size[1] - 2) // 4)
        self.stdscr.addstr(y_offset, x_offset, title)

    def __draw_tiles(self, state):
        tile_to_display_char = {
            Tiles.EMPTY: ' ',
            Tiles.ORB: 'o',
            Tiles.PLAYER_TAIL: curses.ACS_BLOCK,
        }

        for y in range(0, self.config.arena_size[1]):
            for x in range(0, self.config.arena_size[0]):
                tile = state.arena[x][y]
                display_char = tile_to_display_char[tile]
                try:
                    self.arena_win.addch(y, x, display_char)
                except (curses.error):
                    # addch() fails at the bottom-right character because it tries
                    # to scroll to a new line but no line exists. Best workaround
                    # I could find.
                    # https://stackoverflow.com/questions/37648557/curses-error-add-wch-returned-an-error
                    pass

    def __draw_player(self, state):
        direction_to_display_char = {
            'U': curses.ACS_UARROW,
            'D': curses.ACS_DARROW,
            'L': curses.ACS_LARROW,
            'R': curses.ACS_RARROW,
        }

        display_char = direction_to_display_char[state.player.direction]
        self.arena_win.addch(state.player.position[1], state.player.position[0], display_char)

    def __draw_message(self, message):
        x_offset = (curses.COLS - len(message)) // 2
        self.message_win.addstr(0, x_offset, message)

    def draw(self, state):
        self.__draw_tiles(state)
        self.__draw_player(state)

        if state.game_over:
            self.__draw_message('Game Over!')
            self.message_win.refresh()

        self.arena_win.box()
        self.arena_win.refresh()
