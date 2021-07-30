from tkinter import *

import numpy as np
import pygame

from settings import *


class Sudoku:
    def __init__(self):

        self.Ongrid = None
        pygame.init()

        self.screen = pygame.display.set_mode((Screenwidth, Screenheight))
        self.running = True
        self.grid = StartBoard
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 50)
        self.text = None
        self.number = None
        self.locked = []
        self.WrongCells = []
        self.emptyCells = []
        self.numbs = np.array(
            self.grid)
        self.startNumber()

        ##BUTTONS##
        self.ButtonColor_Solve = BLUE
        self.ButtonColor_Timer = BLUE
        self.ButtonColor_Clear = BLUE
        self.ButtonColor_Board = BLUE

        ##TIMER##
        self.TimerStarted = False
        self.seconds = 0
        self.minutes = 0
        self.minuteconverted = 0


    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                Ongrid = self.mouseOnBoard()
                if Ongrid:
                    self.Ongrid = Ongrid

                if self.OverButton_Solve:
                    self.BacktrackSolve(self.grid)

                if self.OverButton_Board:
                    self.ChangeBoard()

                if self.OverButton_Timer:
                    if not self.TimerStarted:
                        self.TimerStarted = True
                        self.startTime = pygame.time.get_ticks()

                    elif self.TimerStarted:
                        self.TimerStarted = False




                if self.OverButton_Clear:
                    self.locked.clear()
                    self.numbs = np.zeros((9, 9), dtype=int)
                    self.grid = self.numbs.tolist()
                    self.minuteconverted = 0
                    self.minutes = 0

                    self.startTime = pygame.time.get_ticks()  # Bei Clear wird die Zeit neu erfasst

            if event.type == pygame.KEYDOWN:

                self.number = pygame.key.name(event.key)
                if self.number.isdigit():

                    if list(self.Ongrid) not in self.locked and self.Ongrid is not None:
                        index = (self.Ongrid[1], self.Ongrid[0])  # Sucht die Zahl zum Ändern mit dem Index raus

                        self.numbs[index] = self.number  # Ändert die Zahl zur eingegebenen Zahl

                        self.grid = self.numbs.tolist()  # Konvertiert das numpy array in die self.grid liste

    ######################################################################

    def draw(self):
        self.screen.fill(WHITE)
        if self.Ongrid:
            self.drawSelection(self.screen, self.Ongrid)
        if self.TimerStarted:
            self.Timer()
        else:
            self.drawTimer(self.screen)
        self.lockcells(self.screen, self.locked)
        self.drawNumbers(self.screen)
        self.initButtons(self.screen, self.ButtonColor_Solve, self.ButtonColor_Timer, self.ButtonColor_Clear,
                         self.ButtonColor_Board)
        self.drawGrid(self.screen)
        pygame.display.update()

    #######################################################################

    def drawGrid(self, screen):
        pygame.draw.rect(screen, BLACK, (gridPos[0], gridPos[1], Width - 40, Height - 80), 7)
        for x in range(9):

            if x % 3 != 0:  # e.g. wenn nicht teilbar durch 3

                pygame.draw.line(screen, BLACK, (gridPos[0] + (x * cellsize), gridPos[1]),
                                 (gridPos[0] + (x * cellsize), gridPos[1] + 800))
                pygame.draw.line(screen, BLACK, (gridPos[0], gridPos[1] + (x * cellsize)),
                                 (gridPos[0] + 800, gridPos[1] + (x * cellsize)))
            else:
                pygame.draw.line(screen, BLACK, (gridPos[0] + (x * cellsize), gridPos[1]),
                                 (gridPos[0] + (x * cellsize), gridPos[1] + 800), 7)
                pygame.draw.line(screen, BLACK, (gridPos[0], gridPos[1] + (x * cellsize)),
                                 (gridPos[0] + 800, gridPos[1] + (x * cellsize)), 7)

    def mouseOnBoard(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridsize[0] or self.mousePos[1] > gridPos[1] + gridsize[1]:
            return False
        return (self.mousePos[0] - gridPos[0]) // cellsize, (self.mousePos[1] - gridPos[
            1]) // cellsize

    def drawSelection(self, screen, pos):
        # Paints selected Square grey
        pygame.draw.rect(screen, GREY,
                         (pos[0] * cellsize + gridPos[0], pos[1] * cellsize + gridPos[1], cellsize, cellsize))

    def drawNumbers(self, screen):
        # Draws all gridnumbers
        for ypos, row in enumerate(self.grid):
            for xpos, num in enumerate(row):
                if num != 0:
                    pos = [xpos * cellsize + gridPos[0] + cellsize * 0.37,
                           ypos * cellsize + gridPos[1] + cellsize * 0.25]

                    self.drawNumbersToScreen(screen, num, pos)

    def startNumber(self):
        # Gets all numbers from the Starting Board to lock them, making them unchangeable
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.locked.append([xidx, yidx])

    def lockcells(self, screen, locked):
        # Paints all locked cells orange
        for cells in locked:
            pygame.draw.rect(screen, ORANGE,
                             (cells[0] * cellsize + gridPos[0], cells[1] * cellsize + gridPos[1], cellsize, cellsize))

    def drawNumbersToScreen(self, screen, num, pos):
        numbersurface = self.font.render(str(num), False, BLACK)
        screen.blit(numbersurface, pos)

    def ChangeBoard(self):
        # GUI Setup to Drag and Drop while forbidding to close or minimize the Window
        root = Tk()
        root.after(1, lambda: root.focus_force())  # for some reason root.focus_force only works with this lambda
        root.attributes("-topmost", True)
        root.offsetx = 0
        root.offsety = 0

        def dragWindow(event):
            x = root.winfo_pointerx() - root.offsetx
            y = root.winfo_pointery() - root.offsety
            root.geometry(f"+{x}+{y}")

        def clickWindow(event):
            root.offsetx = event.x + event.widget.winfo_rootx() - root.winfo_rootx()  # Stops the window from jumping
            root.offsety = event.y + event.widget.winfo_rooty() - root.winfo_rooty()

        root.overrideredirect(True)  # This makes clickWindow and dragWindow a necessity
        root.bind("<ButtonPress-1>", clickWindow)
        root.bind('<B1-Motion>', dragWindow)

        ############################################################################
        values = list()
        E = dict()
        T = dict()
        textinput = dict()

        def focus_next(event, i):
            event.widget.tk_focusNext().focus()

        def on_focus(event, i):
            # Focused Entries will be emptied and can be used for input
            if E[i].get() == "0":
                E[i].delete(0, "end")
                E[i].insert(0, "")
                E[i].config(fg="black")

        def on_focus_out(event, i):
            # Unfocused Entries get set to 0
            if E[i].get() == "":
                E[i].insert(0, "0")
                E[i].config(fg="grey")

        define_lambda_focus_next = lambda i: (lambda event: focus_next(event,
                                                                       i))  # define the lambdas in the for loop instead of defining them at execution
        define_lambda_on_focus = lambda i: (lambda event: on_focus(event, i))
        define_lambda_on_focus_out = lambda i: (lambda event: on_focus_out(event, i))

        for ypos, row in enumerate(self.grid):
            for xpos, num in enumerate(row):
                i = (ypos * 9) + (
                            xpos + 1)  # enumerate startet bei 0 also kann xpos als auch ypos 0 sein, was zu i = 0 führt

                textinput[i] = StringVar()
                E[i] = Entry(root, textvariable=textinput[i], font="Arial 10", width=2, fg="grey", justify="center")
                E[i].insert(0, "0")

                E[i].bind("<Return>", define_lambda_focus_next(i))  # lambdas are defined lazily....i = 9
                E[i].bind("<FocusIn>", define_lambda_on_focus(i))
                E[i].bind("<FocusOut>", define_lambda_on_focus_out(i))

                E[i].grid(row=ypos, column=xpos + 2)  # xpos +2 because labels are at column 1

                T[i] = Label(root, text=f"Row {ypos + 1}")

                T[i].grid(row=ypos,
                          column=1)  # i as row, otherwise it has a weird offset

        def quitTK():

            for i in range(1, 82):

                try:
                    values.append(int(textinput[i].get()))
                except:
                    values.append(0)

            split_values = np.array(np.array_split(values, 9))
            split_values_list = split_values.tolist()

            self.grid = split_values_list
            self.locked.clear()
            self.startNumber()

            root.destroy()

        confirm = Button(root, text="Confirm Changes", command=quitTK)
        confirm.grid(column=1)

        root.mainloop()

    #################################TIMER#################################

    def Timer(self):
        self.seconds = (pygame.time.get_ticks() - self.startTime - self.minuteconverted * 1000) // 1000
        if self.seconds == 60:
            self.minuteconverted = (self.minuteconverted + 60)
            self.minutes = self.minutes + 1
        self.drawTimer(self.screen)

    def drawTimer(self, screen):
        TimerSeconds = self.font.render(str(self.seconds), False, BLACK)
        screen.blit(TimerSeconds, (gridPos[0] + 635, gridPos[1] + gridsize[1] + 50, 200, 50))
        TimerMinutes = self.font.render(str(self.minutes), False, BLACK)
        screen.blit(TimerMinutes, (gridPos[0] + 555, gridPos[1] + gridsize[1] + 50, 200, 50))
        TimerDoppelPunkt = self.font.render(":", False, BLACK)
        screen.blit(TimerDoppelPunkt, (gridPos[0] + 617, gridPos[1] + gridsize[1] + 47, 200, 50))

    #################################BUTTONS#################################

    def initButtons(self, screen, ButtonColor_Solve, ButtonColor_Timer, ButtonColor_Clear, ButtonColor_Board):
        pygame.draw.rect(screen, ButtonColor_Solve, (gridPos[0], gridPos[1] + gridsize[1] + 20, 200, 50))
        pygame.draw.rect(screen, ButtonColor_Timer, (gridPos[0] + 300, gridPos[1] + gridsize[1] + 20, 200, 50))
        pygame.draw.rect(screen, ButtonColor_Clear, (gridPos[0] + 300, gridPos[1] + gridsize[1] + 100, 200, 50))
        pygame.draw.rect(screen, ButtonColor_Board, (gridPos[0], gridPos[1] + gridsize[1] + 100, 200, 50))

        ButtonSurface_Solve = self.font.render("Solve", False, ORANGE)
        ButtonSurface_Timer = self.font.render("Timer", False, ORANGE)
        ButtonSurface_Clear = self.font.render("Clear", False, ORANGE)
        ButtonSurface_Board = self.font.render("Board", False, ORANGE)

        screen.blit(ButtonSurface_Solve, (gridPos[0] + 35, gridPos[1] + gridsize[1] + 20, 200, 50))
        screen.blit(ButtonSurface_Timer, (gridPos[0] + 335, gridPos[1] + gridsize[1] + 20, 200, 50))
        screen.blit(ButtonSurface_Clear, (gridPos[0] + 335, gridPos[1] + gridsize[1] + 100, 200, 50))
        screen.blit(ButtonSurface_Board, (gridPos[0] + 35, gridPos[1] + gridsize[1] + 100, 200, 50))

        self.checkButtons()

    def checkButtons(self):
        if gridPos[0] + 200 > self.mousePos[0] > gridPos[0] and gridPos[1] + gridsize[1] + 70 > self.mousePos[1] > \
                gridPos[1] + gridsize[1] + 20:
            self.OverButton_Solve = True

            self.ButtonColor_Solve = GREEN
        else:
            self.ButtonColor_Solve = BLUE
            self.OverButton_Solve = False
        if gridPos[0] + 500 > self.mousePos[0] > gridPos[0] + 300 and gridPos[1] + gridsize[1] + 70 > self.mousePos[
            1] > \
                gridPos[1] + gridsize[1] + 20:
            self.OverButton_Timer = True
            self.ButtonColor_Timer = GREEN
        else:
            self.ButtonColor_Timer = BLUE
            self.OverButton_Timer = False
        if gridPos[0] + 500 > self.mousePos[0] > gridPos[0] + 300 and gridPos[1] + gridsize[1] + 150 > self.mousePos[
            1] > \
                gridPos[1] + gridsize[1] + 100:
            self.ButtonColor_Clear = GREEN
            self.OverButton_Clear = True
        else:
            self.ButtonColor_Clear = BLUE
            self.OverButton_Clear = False
        if gridPos[0] + 200 > self.mousePos[0] > gridPos[0] and gridPos[1] + gridsize[1] + 150 > self.mousePos[1] > \
                gridPos[1] + gridsize[1] + 100:
            self.OverButton_Board = True
            self.ButtonColor_Board = GREEN
        else:
            self.ButtonColor_Board = BLUE
            self.OverButton_Board = False

    #################################SOLVER#################################

    def BacktrackSolve(self, grid):
        found = self.find_emptyCell(grid)

        if not found:
            return True
        else:
            row, col = found
        for i in range(1, 10):
            if self.Check(grid, i, (row, col)):
                grid[row][col] = i

                if self.BacktrackSolve(grid):
                    return True
                grid[row][col] = 0

        return False

    def find_emptyCell(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def Check(self, grid, num, pos):
        # Checks if the numberinput is valid
        for i in range(9):
            if grid[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(9):
            if grid[i][pos[1]] == num and pos[0] != i:
                return False

        sq_x = pos[1] // 3
        sq_y = pos[0] // 3

        for i in range(sq_y * 3, sq_y * 3 + 3):
            for j in range(sq_x * 3, sq_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False
        return True

    def update(self):
        self.mousePos = pygame.mouse.get_pos()


#################################################################################################


app = Sudoku()
app.run()
##
