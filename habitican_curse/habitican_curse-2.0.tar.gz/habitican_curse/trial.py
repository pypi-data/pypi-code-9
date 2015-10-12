import curses
import tempfile
import locale

locale.setlocale(locale.LC_ALL, '') 
def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    stdscr.bkgd(' ', curses.color_pair(1))
    for i in range(0, curses.COLORS):
        if i%2==0:
	    curses.init_pair(i + 1, i, 236)
	else:
	    curses.init_pair(i+1, i, 0)
    try:
        for i in range(0, 255):
            stdscr.addstr(str(i), curses.color_pair(i-1)|curses.A_BOLD)
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)
