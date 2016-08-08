import curses
from game import Input

class CursesInputSource:
    """Defines a game input source using curses input."""
    def __init__(self, stdscr):
        """Creates a new CursesInputSource.

        stdscr: A curses main window object, as obtained from curses.wrapper() or curses.iniscr()
        """
        self.key_to_action = {
            curses.KEY_UP: 'PLAYER_UP',
            curses.KEY_DOWN: 'PLAYER_DOWN',
            curses.KEY_LEFT: 'PLAYER_LEFT',
            curses.KEY_RIGHT: 'PLAYER_RIGHT',
        }
        self.stdscr = stdscr

    def get_input(self):
        """Gets an input event."""
        input_key = self.stdscr.getch()
        if input_key in self.key_to_action:
            return Input(self.key_to_action[input_key], True)
        elif input_key == curses.ERR:
            return Input(None, False)
        else:
            return Input(None, True)
