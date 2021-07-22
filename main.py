import curses
from curses import textpad
import time

def sudoku(win):
    curses.curs_set(0) #Disable cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    version = "v0.1"
    h, w = win.getmaxyx() #Get window size
    box = [[1, 2], [h - 1, w - 2]]
    boxYN = [[h//2 - 6, w//2 - 21], [h//2 + 4, w//2 + 21]]
    grid = [[0 for i in range(9)] for i in range(9)] #Initialise empty sudoku
    gridLock = [[False for i in range(9)] for i in range(9)]
    grid[3][3] = 3
    grid[4][4] = 4
    gridLock[3][3] = True
    cursor = [0, 0]

    def printGrid(): #Print the sudoku
        win.attron(curses.color_pair(5))
        textpad.rectangle(win, box[0][0], box[0][1], box[1][0], box[1][1])
        win.addstr(h//2 - 16, w//2 - 8, "Lucky Sudoku Solver")
        win.addstr(h//2 - 15, w//2 - 1, version)
        win.addstr(h//2 + 12, w//2 - 40, "[F7] : Solve sudoku")
        win.addstr(h//2 + 13, w//2 - 47, "[BACKSPACE] : Reset case")
        win.addstr(h//2 + 14, w//2 - 43, "[ENTER] : Lock/Unlock case")
        win.addstr(h//2 + 15, w//2 - 40, "[F2] : Clear all")
        win.addstr(h//2 + 16, w//2 - 40, "[F1] : Quit")
        win.attroff(curses.color_pair(5))
        for i in range(9): #Y
            for j in range(9): #X
                if gridLock[i][j]:
                    win.attron(curses.color_pair(2))
                if cursor == [i, j]:
                    win.attron(curses.color_pair(1))
                if(grid[i][j] != 0): #Used case
                    win.addstr(getY(i), getX(j), str(grid[i][j]))
                else: #Empty case
                    win.addstr(getY(i), getX(j), ".")
                win.attroff(curses.color_pair(1))
                win.attroff(curses.color_pair(2))
        for i in range(2): #2 horizontal lines
            for j in range(53): #53 char
                win.addstr((getY(((i + 1) * 3) - 1) + 2), (getX(0) + j - 4), "-")
        for i in range(2): #3 vertical lines
            for j in range(23): #23 char
                win.addstr((getY(0) + j - 1), (getX(((i + 1) * 3) - 1) + 4), "|")
        win.refresh() #Update screen
    
    def printCase(y = cursor[0], x = cursor[1]):
        if gridLock[y][x]:
            win.attron(curses.color_pair(2))
        if cursor == [y, x]:
            win.attron(curses.color_pair(1))
        if(grid[y][x] != 0): #Used case
            win.addstr(getY(y), getX(x), str(grid[y][x]))
        else: #Empty case
            win.addstr(getY(y), getX(x), ".")
        win.attroff(curses.color_pair(1))
        win.attroff(curses.color_pair(2))
        win.refresh()
    
    def getX(row): #row = 0 to 9
        return w//2 - (5 * (4 - row)) + (-2 if row < 3 else (2 if row > 5 else 0))
    def getY(col): #col = 0 to 9
        return h//2 - (2 * (4 - col)) + (-2 if col < 3 else (2 if col > 5 else 0))
    
    def askYN(message):
        win.clear()
        win.attron(curses.color_pair(5))
        textpad.rectangle(win, boxYN[0][0], boxYN[0][1], boxYN[1][0], boxYN[1][1])
        win.addstr(h//2 - 16, w//2 - 8, "Lucky Sudoku Solver")
        win.addstr(h//2 - 15, w//2 - 1, version)
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
    
    def log(message:str = "", color:int = 0):
        if message == "":
            message = "                            "
        if color > 0 and color <= 4:
            win.attron(curses.color_pair(color))
            win.addstr(h//2 + 14, w//2 - len(message)//2, message)
            win.attroff(curses.color_pair(color))
        else:
            win.addstr(h//2 + 14, w//2 - len(message)//2, message)
        win.addstr(h//2 + 14, w//2 + len(message)//2 + 1, "                     ")
        win.refresh()

    printGrid()
    log("Started")

    running = True
    while(running):
        key = win.getch()
        if key == curses.KEY_UP:
            if cursor[0] > 0:
                cursor[0] -= 1
                printCase((cursor[0] + 1), cursor[1]) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
            elif cursor[0] == 0:
                cursor[0] = 8
                printCase(0, cursor[1]) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
        elif key == curses.KEY_DOWN:
            if cursor[0] < 8:
                cursor[0] += 1
                printCase((cursor[0] - 1), cursor[1]) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
            elif cursor[0] == 8:
                cursor[0] = 0
                printCase(8, cursor[1]) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
        elif key == curses.KEY_LEFT:
            if cursor[1] > 0:
                cursor[1] -= 1
                printCase(cursor[0], cursor[1] + 1) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
            elif cursor[1] == 0:
                cursor[1] = 8
                printCase(cursor[0], 0) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
        elif key == curses.KEY_RIGHT:
            if cursor[1] < 8:
                cursor[1] += 1
                printCase(cursor[0], cursor[1] - 1) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
            elif cursor[1] == 8:
                cursor[1] = 0
                printCase(cursor[0], 8) #Reset old case
                printCase(cursor[0], cursor[1]) #Print new case
                log()
        elif key == curses.KEY_BACKSPACE:
            if not gridLock[cursor[0]][cursor[1]]:
                grid[cursor[0]][cursor[1]] = 0
                log("Case reset")
                printCase(cursor[0], cursor[1]) #Print case
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if grid[cursor[0]][cursor[1]] != 0:
                gridLock[cursor[0]][cursor[1]] = not gridLock[cursor[0]][cursor[1]]
                log(("Case locked" if gridLock[cursor[0]][cursor[1]] else "Case unlocked"), (2 if gridLock[cursor[0]][cursor[1]] else 0))
        elif key >= 49 and key <= 57:
            if not gridLock[cursor[0]][cursor[1]]:
                grid[cursor[0]][cursor[1]] = key - 48
                printCase(cursor[0], cursor[1]) #Print case
        elif key == curses.KEY_F2:
            if askYN("Clear the entire sudoku?"):
                grid = [[0 for i in range(9)] for i in range(9)]
                gridLock = [[False for i in range(9)] for i in range(9)]
            printGrid()
        elif key == curses.KEY_F1:
            choice = askYN("Are you sure you want to quit?")
            if choice:
                win.attron(curses.color_pair(5))
                textpad.rectangle(win, h//2 - 2, w//2 - 7, h//2 + 2, w//2 + 7)
                win.attroff(curses.color_pair(5))
                win.addstr(h//2, w//2 - 3, "Bye! :)")
                win.refresh()
                time.sleep(1)
                running = False
            else:
                printGrid()

if __name__ == "__main__":
    curses.wrapper(sudoku) #Start Lucky-Sudoku-Solver