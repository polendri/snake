import curses
from game import Input

class CursesInputSource:
    def __init__(self, stdscr):
        self.key_to_action = {
            curses.KEY_UP: 'PLAYER_UP',
            curses.KEY_DOWN: 'PLAYER_DOWN',
            curses.KEY_LEFT: 'PLAYER_LEFT',
            curses.KEY_RIGHT: 'PLAYER_RIGHT',
        }
        self.stdscr = stdscr

    def get_input(self):
        input_key = self.stdscr.getch()
        if input_key in self.key_to_action:
            return Input(self.key_to_action[input_key], True)
        elif input_key == curses.ERR:
            return Input(None, False)
        else:
            return Input(None, True)
