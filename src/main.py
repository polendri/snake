import curses
from display import CursesDisplay
from game import Config

def main(stdscr):
    config = Config()
    display = CursesDisplay(stdscr, config)
    display.draw(None)

if __name__ == '__main__':
    curses.wrapper(main)
