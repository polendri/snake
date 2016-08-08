import curses
from display import CursesDisplay
from input_source import CursesInputSource
from game import Config, Game, State

def main(stdscr):
    config = Config(
        arena_size=(80,40),
        orb_count=3,
        tick_rate=8
    )
    display = CursesDisplay(stdscr, config)
    input_source = CursesInputSource(stdscr)
    game = Game(config, display, input_source)
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)
