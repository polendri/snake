import curses

class CursesDisplay:
    def __init__(self, stdscr, config):
        curses.curs_set(0)

        width = config.arena_size[0] + 2
        height = config.arena_size[ 1] + 2
        x_offset = max(1, (curses.COLS - config.arena_size[0]) // 2)
        y_offset = max(1, (curses.LINES - config.arena_size[1]) // 2)
        self.config = config
        self.stdscr = stdscr
        self.arena_win = curses.newwin(
            config.arena_size[1],
            config.arena_size[0],
            y_offset,
            x_offset)

        self.__draw_arena_border((x_offset, y_offset))

    def __draw_arena_border(self, offset):
        x_min = offset[0] - 1
        x_max = offset[0] + self.config.arena_size[0] + 1
        y_min = offset[1] - 1
        y_max = offset[1] + self.config.arena_size[1] + 1

        # Draw corners
        corner_char = '+'
        self.stdscr.addch(y_min, x_min, corner_char)
        self.stdscr.addch(y_min, x_max, corner_char)
        self.stdscr.addch(y_max, x_min, corner_char)
        self.stdscr.addch(y_max, x_max, corner_char)

        # Draw edges
        horizontal_edge_char = '-'
        vertical_edge_char = '|'
        for i in range(x_min + 1, x_max):
            self.stdscr.addch(y_min, i, horizontal_edge_char)
            self.stdscr.addch(y_max, i, horizontal_edge_char)
        for i in range(y_min + 1, y_max):
            self.stdscr.addch(i, x_min, vertical_edge_char)
            self.stdscr.addch(i, x_max, vertical_edge_char)

    def draw(self, state):
        self.stdscr.getch()
