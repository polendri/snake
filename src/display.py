import curses
from game import Tiles

class CursesDisplay:
    def __init__(self, stdscr, config):
        curses.curs_set(0)

        width = config.arena_size[0] + 2
        height = config.arena_size[1] + 2
        x_offset = max(1, (curses.COLS - config.arena_size[0]) // 2)
        y_offset = max(3, (curses.LINES - config.arena_size[1]) // 2)
        self.config = config
        self.stdscr = stdscr
        self.arena_win = curses.newwin(
            config.arena_size[1],
            config.arena_size[0],
            y_offset,
            x_offset)

        self.__draw_title()
        self.stdscr.refresh()

    def __draw_title(self):
        title = 'SNAAAAKE'
        x_offset = (curses.COLS - len(title)) // 2
        y_offset = max(1, (curses.LINES - self.config.arena_size[1] - 2) // 4)
        self.stdscr.addstr(y_offset, x_offset, title)

    def draw(self, state):
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

        self.arena_win.box()
        self.arena_win.refresh()
        self.stdscr.getch()
