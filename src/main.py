import curses
from display import CursesDisplay
from game import Config, State

def main(stdscr):
    config = Config()
    display = CursesDisplay(stdscr, config)
    state = State(config)
    state.spawn_orb()
    state.spawn_orb()
    state.spawn_orb()
    display.draw(state)

if __name__ == '__main__':
    curses.wrapper(main)
