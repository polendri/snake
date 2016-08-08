import curses
from display import CursesDisplay

def main(stdscr):
    display = CursesDisplay(stdscr)
    display.draw_test()

if __name__ == '__main__':
    curses.wrapper(main)
