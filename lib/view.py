import curses
from curses import textpad

from lib.settings import version

def init(win):
    global h, w, box, boxYN
    h, w = win.getmaxyx()
    box = [[1, 2], [h - 1, w - 2]]
    boxYN = [[h//2 - 6, w//2 - 21], [h//2 + 4, w//2 + 21]]

def printGrid(win, grid, gridLock, cursor): #Print the sudoku
    win.clear()
    win.attron(curses.color_pair(5))
    textpad.rectangle(win, box[0][0], box[0][1], box[1][0], box[1][1])
    win.addstr(h//2 - 16, w//2 - 8, "Lucky Sudoku Solver")
    win.addstr(h//2 - 15, w//2 - len(version)//2, version)
    win.addstr(h//2 - 12, w//2 - 35, "[F7] : Solve sudoku")
    win.addstr(h//2 - 13, w//2 - 42, "[BACKSPACE] : Reset case")
    win.addstr(h//2 - 14, w//2 - 38, "[ENTER] : Lock/Unlock case")
    win.addstr(h//2 - 15, w//2 - 35, "[F2] : Clear all")
    win.addstr(h//2 - 16, w//2 - 35, "[F1] : Menu")
    win.attroff(curses.color_pair(5))
    for i in range(9): #Y
        for j in range(9): #X
            if gridLock[i][j]:
                win.attron(curses.color_pair(6))
            if cursor == [i, j]:
                win.attron(curses.color_pair(1))
            if(grid[i][j] != 0): #Used case
                win.addstr(getY(i), getX(j), str(grid[i][j]))
            else: #Empty case
                win.addstr(getY(i), getX(j), ".")
            win.attroff(curses.color_pair(1))
            win.attroff(curses.color_pair(6))
    for i in range(2): #2 horizontal lines
        for j in range(53): #53 char
            win.addstr((getY(((i + 1) * 3) - 1) + 2), (getX(0) + j - 4), "-")
    for i in range(2): #3 vertical lines
        for j in range(23): #23 char
            win.addstr((getY(0) + j - 1), (getX(((i + 1) * 3) - 1) + 4), "|")
    win.refresh() #Update screen

def printCase(win, grid, gridLock, cursor, y, x, solving = False):
    if solving:
        win.attron(curses.color_pair(5))
    else:
        if gridLock[y][x]:
            win.attron(curses.color_pair(6))
        if cursor == [y, x]:
            win.attron(curses.color_pair(1))
    if(grid[y][x] != 0): #Used case
        win.addstr(getY(y), getX(x), str(grid[y][x]))
    else: #Empty case
        win.addstr(getY(y), getX(x), ".")
    win.attroff(curses.color_pair(1))
    win.attroff(curses.color_pair(5))
    win.attroff(curses.color_pair(6))
    win.refresh()

def getX(row): #row = 0 to 9
    return w//2 - (5 * (4 - row)) + (-2 if row < 3 else (2 if row > 5 else 0))
def getY(col): #col = 0 to 9
    return h//2 - (2 * (4 - col)) + (-2 if col < 3 else (2 if col > 5 else 0))

def askYN(win, message):
    win.clear()
    win.attron(curses.color_pair(5))
    textpad.rectangle(win, h//2 - 6, w//2 - len(message)//2 - 5, h//2 + 4, w//2 + len(message)//2 + 5)
    win.addstr(h//2 - 16, w//2 - 8, "Lucky Sudoku Solver")
    win.addstr(h//2 - 15, w//2 - len(version)//2, version)
    win.attroff(curses.color_pair(5))
    win.addstr(h//2 - 3, w//2 - len(message)//2, message)
    choice = False
    waiting = True
    while(waiting):
        if(choice):
            win.attron(curses.color_pair(2))
            win.addstr(h//2, w//2 - 9, "[ YES ]")
            win.attroff(curses.color_pair(3))
            win.addstr(h//2, w//2 + 2, "  NO!  ")
        else:
            win.attron(curses.color_pair(4))
            win.addstr(h//2, w//2 + 2, "[ NO! ]")
            win.attroff(curses.color_pair(3))
            win.addstr(h//2, w//2 - 9, "  YES  ")
        win.refresh()
        key = win.getch()
        if key == curses.KEY_LEFT:
            choice = True
        elif key == curses.KEY_RIGHT:
            choice = False
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            waiting = False
    win.clear()
    return choice

def printSolved(win, grid, solved, tries):
    current = 0
    choice = 1 if len(solved) > 1 else 0
    waiting = True
    while waiting:
        win.clear()
        win.attron(curses.color_pair(5))
        textpad.rectangle(win, box[0][0], box[0][1], box[1][0], box[1][1])
        win.addstr(h//2 - 16, w//2 - 8, "Lucky Sudoku Solver")
        win.addstr(h//2 - 15, w//2 - len(version)//2, version)
        win.addstr(h//2 + 13, w//2 - 38, "Number of tries: " + str(tries[0]))
        win.addstr(h//2 + 14, w//2 - 42, "Number of solutions: " + str(len(solved)))
        win.addstr(h//2 + 16, w//2 - 32, "[F1] : Back")
        win.attroff(curses.color_pair(5))
        for i in range(9): #Y
            for j in range(9): #X
                if grid[i][j] == 0:
                    win.attron(curses.color_pair(2))
                win.addstr(getY(i), getX(j), str(solved[current][i][j]))
                win.attroff(curses.color_pair(2))
        for i in range(2): #2 horizontal lines
            for j in range(53): #53 char
                win.addstr((getY(((i + 1) * 3) - 1) + 2), (getX(0) + j - 4), "-")
        for i in range(2): #3 vertical lines
            for j in range(23): #23 char
                win.addstr((getY(0) + j - 1), (getX(((i + 1) * 3) - 1) + 4), "|")
        if current > 0:
            if choice == - 1:
                win.attron(curses.color_pair(2))
            win.addstr(h//2 + 14, w//2 - 17, "[ <Previous ]")
            win.attroff(curses.color_pair(2))
        if current < len(solved) - 1:
            if choice == 1:
                win.attron(curses.color_pair(2))
            win.addstr(h//2 + 14, w//2 + 8, "[ Next> ]")
        win.attroff(curses.color_pair(2))
        win.addstr(h//2 + 14, w//2 - 1, str(current + 1) + "/" + str(len(solved)))
        win.refresh() #Update screen
        key = win.getch()
        if key == curses.KEY_LEFT:
            if current > 0:
                choice = -1
        elif key == curses.KEY_RIGHT:
            if current < len(solved) - 1:
                choice = 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if choice == -1 and current > 0:
                current -= 1
                if current == 0:
                    choice = 1
            elif choice == 1 and current < len(solved) - 1:
                current += 1
                if current == len(solved) - 1:
                    choice = -1
        elif key == curses.KEY_F1:
            waiting = False

def log(win, message:str = "", color:int = 0):
    win.addstr(h//2 + 14, w//2 - 35//2, "                                   ")
    win.refresh()
    if message == "":
        message = "                                   "
    if color > 0 and color <= 4:
        win.attron(curses.color_pair(color))
        win.addstr(h//2 + 14, w//2 - len(message)//2, message)
        win.attroff(curses.color_pair(color))
    else:
        win.addstr(h//2 + 14, w//2 - len(message)//2, message)
    win.addstr(h//2 + 14, w//2 + len(message)//2 + 1, "                     ")
    win.refresh()

def bye(win):
    win.attron(curses.color_pair(5))
    textpad.rectangle(win, h//2 - 2, w//2 - 7, h//2 + 2, w//2 + 7)
    win.attroff(curses.color_pair(5))
    win.addstr(h//2, w//2 - 3, "Bye! :)")
    win.refresh()