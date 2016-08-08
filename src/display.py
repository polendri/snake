import curses

class CursesDisplay:
    def __init__(self, stdscr):
        self.stdscr = stdscr
    def draw_test(self):
        self.stdscr.addstr(10, 10, 'Hello world')
        self.stdscr.getch()
