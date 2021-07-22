import curses
from time import sleep

import lib.util as util
import lib.settings as settings
from lib.settings import version, pwd, lang, oneSolution, timeLimit
import lib.view as view
import lib.menu as menu

def sudoku(win):
    curses.curs_set(0) #Disable cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)

    grid = [[0 for i in range(9)] for i in range(9)] #Initialise empty sudoku
    gridLock = [[False for i in range(9)] for i in range(9)]
    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0]
          , [6, 0, 0, 1, 9, 5, 0, 0, 0]
          , [0, 0, 8, 0, 0, 0, 0, 6, 0]
          , [8, 0, 0, 0, 6, 0, 0, 0, 3] #Test grid
          , [4, 0, 0, 8, 0, 3, 0, 0, 1] #With 15 solutions
          , [7, 0, 0, 0, 2, 0, 0, 0, 6]
          , [0, 6, 0, 0, 0, 0, 2, 0, 0]
          , [0, 0, 0, 4, 1, 9, 0, 0, 5]
          , [0, 0, 0, 0, 8, 0, 0, 0, 0]]
    cursor = [4, 4]
    solved = []
    tries = [0]

    view.init(win)

    def possible(y, x, nbr, solving=False):
        for i in range(9):
            if grid[y][i] == nbr:
                if not solving:
                    view.log(win, "Nope", 4)
                    win.attron(curses.color_pair(4))
                    win.addstr(view.getY(y), view.getX(i), str(grid[y][i]))
                    win.attroff(curses.color_pair(4))
                    win.refresh()
                    sleep(1)
                    view.printGrid(win, grid, gridLock, cursor)
                return False #Number already in row
            if grid[i][x] == nbr:
                if not solving:
                    view.log(win, "Nope", 4)
                    win.attron(curses.color_pair(4))
                    win.addstr(view.getY(i), view.getX(x), str(grid[i][x]))
                    win.attroff(curses.color_pair(4))
                    win.refresh()
                    sleep(1)
                    view.printGrid(win, grid, gridLock, cursor)
                return False #Number already in column
            yBox = (y//3) * 3
            xBox = (x//3) * 3
            for i in range(3):
                for j in range(3):
                    if grid[yBox + i][xBox + j] == nbr:
                        if not solving:
                            view.log(win, "Nope", 4)
                            win.attron(curses.color_pair(4))
                            win.addstr(view.getY(yBox + i), view.getX(xBox + j), str(grid[yBox + i][xBox + j]))
                            win.attroff(curses.color_pair(4))
                            win.refresh()
                            sleep(1)
                            view.printGrid(win, grid, gridLock, cursor)
                        return False #Number already in box
        return True #Possible
    
    def solve():
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for nbr in range(1, 10):
                        if possible(i, j, nbr, True):
                            grid[i][j] = nbr
                            tries[0] += 1
                            view.printCase(win, grid, gridLock, cursor, i, j, True)
                            view.log(win, "Tries: " + str(tries[0]), 5)
                            solve()
                            grid[i][j] = 0
                            view.printCase(win, grid, gridLock, cursor, i, j, True)
                    return
        solved.append([])
        for i in range(9):
            solved[len(solved) - 1].append(grid[i].copy())
        solved[len(solved) - 1] = [row[:] for row in grid]

    view.printGrid(win, grid, gridLock, cursor)
    view.log(win, "Started")

    running = True
    while(running):
        key = win.getch()
        if key == curses.KEY_UP:
            if cursor[0] > 0:
                cursor[0] -= 1
                view.printCase(win, grid, gridLock, cursor, (cursor[0] + 1), cursor[1]) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
            elif cursor[0] == 0:
                cursor[0] = 8
                view.printCase(win, grid, gridLock, cursor, 0, cursor[1]) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
        elif key == curses.KEY_DOWN:
            if cursor[0] < 8:
                cursor[0] += 1
                view.printCase(win, grid, gridLock, cursor, (cursor[0] - 1), cursor[1]) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
            elif cursor[0] == 8:
                cursor[0] = 0
                view.printCase(win, grid, gridLock, cursor, 8, cursor[1]) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
        elif key == curses.KEY_LEFT:
            if cursor[1] > 0:
                cursor[1] -= 1
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1] + 1) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
            elif cursor[1] == 0:
                cursor[1] = 8
                view.printCase(win, grid, gridLock, cursor, cursor[0], 0) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
        elif key == curses.KEY_RIGHT:
            if cursor[1] < 8:
                cursor[1] += 1
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1] - 1) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
            elif cursor[1] == 8:
                cursor[1] = 0
                view.printCase(win, grid, gridLock, cursor, cursor[0], 8) #Reset old case
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print new case
                view.log(win)
        elif key == curses.KEY_BACKSPACE:
            if not gridLock[cursor[0]][cursor[1]] and grid[cursor[0]][cursor[1]] != 0:
                grid[cursor[0]][cursor[1]] = 0
                view.log(win, "Case reset")
                view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print case
            else:
                view.log(win, "Case is locked [x]", 4)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if grid[cursor[0]][cursor[1]] != 0:
                gridLock[cursor[0]][cursor[1]] = not gridLock[cursor[0]][cursor[1]]
                view.log(win, ("Case locked [x]" if gridLock[cursor[0]][cursor[1]] else "Case unlocked [ ]"), (6 if gridLock[cursor[0]][cursor[1]] else 0))
        elif key >= 49 and key <= 57:
            nbr = key - 48
            if not gridLock[cursor[0]][cursor[1]]:
                if grid[cursor[0]][cursor[1]] != nbr and possible(cursor[0], cursor[1], nbr):
                    grid[cursor[0]][cursor[1]] = nbr
                    view.printCase(win, grid, gridLock, cursor, cursor[0], cursor[1]) #Print case
            else:
                view.log(win, "Case is locked [x]", 4)
        elif key == curses.KEY_F2:
            if view.askYN(win, "Clear the entire sudoku?"):
                grid = [[0 for i in range(9)] for i in range(9)]
                gridLock = [[False for i in range(9)] for i in range(9)]
                view.log(win, "Sudoku cleared", 2)
            view.printGrid(win, grid, gridLock, cursor)
        elif key == curses.KEY_F7:
            if view.askYN(win, "Solve this Sudoku?"):
                view.printGrid(win, grid, gridLock, cursor)
                solved.clear()
                tries[0] = 0
                solve()
                if view.askYN(win, str(len(solved)) + " solution(s) found. Do you want to see it?"):
                    view.printSolved(win, grid, solved, tries)
            view.printGrid(win, grid, gridLock, cursor)
        elif key == curses.KEY_F1:
            if menu.start(win, grid, gridLock):
                view.bye(win)
                sleep(0.7)
                running = False
            else:
                view.printGrid(win, grid, gridLock, cursor)

if __name__ == "__main__":
    util.loadConfig()

    curses.wrapper(sudoku)