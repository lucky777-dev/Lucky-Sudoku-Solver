import curses
from curses import textpad

import lib.view as view
from lib.settings import version, lang, oneSolution, timeLimit

def start(win, grid, gridLock):
    win.clear()

    choice = 0
    waiting = True
    while(waiting):
        win.attron(curses.color_pair(5))
        textpad.rectangle(win, view.h//2 - 8, view.w//2 - 17//2 - 5, view.h//2 + 10, view.w//2 + 15//2 + 5)
        win.addstr(view.h//2 - 16, view.w//2 - 8, "Lucky Sudoku Solver")
        win.addstr(view.h//2 - 15, view.w//2 - len(version)//2, version)
        win.attroff(curses.color_pair(5))
        win.addstr(view.h//2 - 6, view.w//2 - 4//2, "Menu")
        win.attron(curses.color_pair(5))
        win.addstr(view.h//2 - 3, view.w//2 - 6, "  Continue  ")
        win.addstr(view.h//2 - 1, view.w//2 - 4, "  Load  ")
        win.addstr(view.h//2 + 1, view.w//2 - 4, "  Save  ")
        win.addstr(view.h//2 + 3, view.w//2 - 6, "  Settings  ")
        win.addstr(view.h//2 + 5, view.w//2 - 4, "  About  ")
        win.addstr(view.h//2 + 7, view.w//2 - 4, "  Exit  ")
        win.attroff(curses.color_pair(5))
        if choice == 0:
            win.attron(curses.color_pair(2))
            win.addstr(view.h//2 - 3, view.w//2 - 6, "[ Continue ]")
            win.attroff(curses.color_pair(2))
        elif choice == 1:
            win.attron(curses.color_pair(2))
            win.addstr(view.h//2 - 1, view.w//2 - 4, "[ Load ]")
            win.attroff(curses.color_pair(2))
        elif choice == 2:
            win.attron(curses.color_pair(2))
            win.addstr(view.h//2 + 1, view.w//2 - 4, "[ Save ]")
            win.attroff(curses.color_pair(2))
        elif choice == 3:
            win.attron(curses.color_pair(2))
            win.addstr(view.h//2 + 3, view.w//2 - 6, "[ Settings ]")
            win.attroff(curses.color_pair(2))
        elif choice == 4:
            win.attron(curses.color_pair(2))
            win.addstr(view.h//2 + 5, view.w//2 - 4, "[ About ]")
            win.attroff(curses.color_pair(2))
        elif choice == 5:
            win.attron(curses.color_pair(2))
            win.addstr(view.h//2 + 7, view.w//2 - 4, "[ Exit ]")
            win.attroff(curses.color_pair(2))

        key = win.getch()
        if key == curses.KEY_UP:
            if choice > 0:
                choice -= 1
        elif key == curses.KEY_DOWN:
            if choice < 5:
                choice += 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if choice == 0:
                win.clear()
                return False
            elif choice == 5:
                if view.askYN(win, "Are you sure you want to quit?"):
                    return True
    win.clear()
    return False