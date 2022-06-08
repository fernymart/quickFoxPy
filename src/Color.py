import curses

class Color():
    def set_color(self, type, color):
        if color == 0:
            curses.init_pair(type, curses.COLOR_RED, curses.COLOR_BLACK)
        elif color == 1:
            curses.init_pair(type, curses.COLOR_GREEN, curses.COLOR_BLACK)
        elif color == 2:
            curses.init_pair(type, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        elif color == 3:
            curses.init_pair(type, curses.COLOR_BLUE, curses.COLOR_BLACK)
        elif color == 4:
            curses.init_pair(type, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        elif color == 5:
            curses.init_pair(type, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def color_options(self, stdscr):
        colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
        for i in range(0, len(colors)):
            stdscr.addstr(f"{i + 1}. {colors[i]}\n")

        stdscr.addstr("7. Go back\n")
        key = stdscr.getkey()

        if key == "7":
            return -1

        try:
            return int(key) - 1
        except:
            return -1