# imports libraries
import pygame
import random
import sys
import math
from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw()  # to hide the main Tkinter window

# each of block is a rectangle block
class Rectangle:  # rectangle class (the car)

    def __init__(self, orientation, size, row, column):
        perSq = 80  # one square is 80x80
        self.startX = column * perSq  # starting x-coordinate
        self.startY = row * perSq  # starting y-coordinate
        self.orientation = orientation
        self.size = size

        if self.orientation == "h":  # for horizontal cars
            length = perSq * size
            self.extendX = length  # How much the x-coordinate extends by
            self.extendY = perSq  # How much the y-coordinate extends by
            self.colour = (0, 255, 0)
            self.startLimitX = 0  # Starting x coordinate of where the car can be positioned
            # Starting y coordinate of where the car can be positioned
            self.startLimitY = self.startY
            # Ending x coordinate of where the car can be positioned
            self.endLimitX = 480 - length + 80
            # Ending x coordinate of where the car can be positioned
            self.endLimitY = self.startY + self.extendY

        else:  # same as above, but for vertical, so swap x and y
            length = perSq * size
            self.extendX = perSq
            self.extendY = length
            self.colour = (0, 0, 255)
            self.startLimitX = self.startX
            self.startLimitY = 0
            self.endLimitX = self.startX + self.extendX
            self.endLimitY = 480 - length + 80

        # if it is the first car (car needed to get across)
        if row == 2 and orientation == "h":
            # make it its own different colour to differentiate
            self.colour = (255, 0, 0)

        self.currentX = self.startX + 0  # current x-coordinate of car
        self.currentY = self.startY + 0  # current y-coordinate of car

        self.rectDrag = False  # boolean if the car is currently being dragged or not
        # make rectangle object
        self.rect = pygame.Rect(self.startX, self.startY,
                                self.extendX, self.extendY)


class RushHour:  # main class

    def __init__(self):

        self.loadGame()
        self.makeRectangles()
        self.turns = 0

        pygame.init()  # run pygame
        surfaceSize = 480
        surface = pygame.display.set_mode(
            (surfaceSize, surfaceSize))  # make display window

        start = True  # if it is beginning of program
        self.inGame = True  # loop condition

        while self.inGame:
            self.ev = pygame.event.poll()  # pygame events
            if self.ev.type == pygame.QUIT:  # if window exited
                self.inGame = False

            elif self.ev.type == pygame.MOUSEBUTTONDOWN:  # if the window has been left-clicked
                self.clickObject()

            elif self.ev.type == pygame.MOUSEBUTTONUP:  # if the window has been released from the left-click
                self.unclickObject()

            elif self.ev.type == pygame.MOUSEMOTION:  # if the lect click is still being clicked
                self.objectMidAir()

            surface.fill((255, 255, 255))  # make the surface white

            for x in range(len(self.rectObjects)):  # for each rectangle
                # colour fill the rectangles
                surface.fill(
                    self.rectObjects[x].colour, self.rectObjects[x].rect)
                # draw rectangles, with black borders
                pygame.draw.rect(surface, (0, 0, 0),
                                 self.rectObjects[x].rect, 5)

            pygame.display.flip()  # display on window

            if start:  # if beginning of program
                # create popup
                messagebox.showinfo(
                    'Welcome!', 'Rush Hour\nGet the red car to the end.\n Click and drag to control the cars.')
                start = False

            self.gameOver()

        pygame.quit()  # quit program

    def clickObject(self):  # when the window is clicked
        for x in range(len(self.rectObjects)):  # for every object
            # if the coordinates of the click is within a rectangle
            if self.rectObjects[x].rect.collidepoint(self.ev.pos):
                self.rectObjects[x].rectDrag = True  # make it be in the air
                self.mouseX, self.mouseY = self.ev.pos  # get current mouse position
                # get different between mouse and rectangle coordinates
                self.offsetX = self.rectObjects[x].rect.x - self.mouseX
                self.offsetY = self.rectObjects[x].rect.y - self.mouseY
                break  # stop the loop

    def objectMidAir(self):  # when the rectangle is being held (in air)
        for x in range(len(self.rectObjects)):  # for each rectangle
            if self.rectObjects[x].rectDrag:  # if the rectangle is in the air
                self.mouseX, self.mouseY = self.ev.pos  # get mouse position
                self.rectObjects[x].rect.x = self.mouseX + \
                    self.offsetX  # get midair rectangle coordinates
                self.rectObjects[x].rect.y = self.mouseY + self.offsetY

    def unclickObject(self):  # when the rectangle is let go
        for x in range(len(self.rectObjects)):  # for each rectangle
            if self.rectObjects[x].rectDrag:  # if the rectangle is in the air

                perSq = 80  # one square is 80x80
                # get the 'row and column' of where the rectangle is
                makeshiftColumn, makeshiftRow = self.rectObjects[x].rect.x / \
                    80, self.rectObjects[x].rect.y / 80
                decimalColumn, decimalRow = makeshiftColumn % 1, makeshiftRow % 1

                # depending on decimal part, whether to round up or round down
                # math.ceil will get rid of decimal part and round up
                # math.floor will get rid of decimal part and round down
                if decimalColumn >= 0.5:
                    jumpX = math.ceil(makeshiftColumn) * perSq
                else:
                    jumpX = math.floor(makeshiftColumn) * perSq
                if decimalRow >= 0.5:
                    jumpY = math.ceil(makeshiftRow) * perSq
                else:
                    jumpY = math.floor(makeshiftRow) * perSq
                # jump is the proposed coordinate following multiples of 80
                # say the midair x-coordinate is something like 146, the jumpX will be 160

                # make a temporary list without the rectangle being held for rectangle comparison
                temporaryRectangles = self.rectObjects * 1
                temporaryRectangles.remove(self.rectObjects[x])

                # get the coordinates in the middle of the rectangle
                middleY = (
                    self.rectObjects[x].startY + self.rectObjects[x].extendY + self.rectObjects[x].startY) / 2
                middleX = (
                    self.rectObjects[x].startX + self.rectObjects[x].extendX + self.rectObjects[x].startX) / 2
                moveAllowed = True  # boolean for allowing the move

                if self.rectObjects[x].orientation == "h":
                    # get the starting square that is needed to be checked for collisions
                    countStart = int(self.rectObjects[x].currentX / 80)
                    # get the last square that is needed to be checked for collision
                    countEnd = int(jumpX / 80)
                    if countStart > countEnd:  # if start is bigger then swap
                        countStart, countEnd = countEnd, countStart

                else:  # same but just for vertical, swap X and Y
                    countStart = int(self.rectObjects[x].currentY / 80)
                    countEnd = int(jumpY / 80)
                    if countStart > countEnd:
                        countStart, countEnd = countEnd, countStart

                # depending on size of car, where to check for collision
                # okay i kind of lied about it being the 'middle', because for size 3 car
                # it would check 1/3 and 2/3 of the rectangle
                if self.rectObjects[x].size == 2:
                    divisor = 2

                else:
                    divisor = 3

                for y in range(len(temporaryRectangles)):  # for each rectangle
                    # for each square between the move
                    for z in range(countStart, countEnd+1):
                        if self.rectObjects[x].orientation == "h":
                            # get the new middle coordinate
                            middleX = (
                                (z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor
                            # for size 3 cars
                            middleX2 = (
                                ((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor) * (divisor-1)
                            # this monster if statement checks whether or not the 'middle' coordinate is between the coordinates of another rectangle or not
                            if ((temporaryRectangles[y].startX <= middleX <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX)) or (temporaryRectangles[y].startX <= middleX2 <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX))) and (temporaryRectangles[y].startY <= middleY <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY)):
                                moveAllowed = False
                                # if there is a collision then it cannot move
                                break
                            else:
                                moveAllowed = True
                        else:  # for vertical, same as above, just swap X and Y
                            middleY = (
                                (z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor
                            middleY2 = (
                                ((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor) * (divisor-1)
                            if (temporaryRectangles[y].startX <= middleX <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX)) and ((temporaryRectangles[y].startY <= middleY <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY)) or (temporaryRectangles[y].startY <= middleY2 <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY))):
                                moveAllowed = False
                                break
                            else:
                                moveAllowed = True

                    if moveAllowed == False:
                        break
                # this semi-monster if statement checks whether the new proposed coordinates of the rectangle is within the limits or not
                # and also checks for collision
                if (self.rectObjects[x].startLimitX <= jumpX < self.rectObjects[x].endLimitX) and (self.rectObjects[x].startLimitY <= jumpY < self.rectObjects[x].endLimitY) and moveAllowed:
                    # update the necessary attributes of the rectangle
                    self.rectObjects[x].rect = pygame.Rect(
                        jumpX, jumpY, self.rectObjects[x].extendX, self.rectObjects[x].extendY)
                    self.rectObjects[x].currentX = jumpX
                    self.rectObjects[x].currentY = jumpY
                    self.rectObjects[x].startX = jumpX
                    self.rectObjects[x].startY = jumpY
                    self.rectObjects[x].rectDrag = False
                    self.turns += 1

                else:  # if it doesnt match
                    # put the rectangle back to where the user moved it from
                    self.rectObjects[x].rect = pygame.Rect(
                        self.rectObjects[x].currentX, self.rectObjects[x].currentY, self.rectObjects[x].extendX, self.rectObjects[x].extendY)
                    self.rectObjects[x].rectDrag = False
                    # error message popup
                    messagebox.showwarning(
                        'Error', 'You cannot make that move.')

    def loadGame(self):  # reading the file
        self.carInfos = []  # list of car information
        filename = str("game0.txt")  # get 2nd file
        file = open(filename, 'r')  # open it
        lines = file.readlines()  # save the file to a list

        for x in range(len(lines)):
            # for each line, get rid of the \n that appears at the end
            lines[x] = lines[x][:-1]

        for line in lines:
            # seperate each data to its own string and add to list
            self.carInfos.append(line.split(', '))

    def makeRectangles(self):  # make rectangle objects
        self.rectObjects = []  # list of rectangle objects
        for each in self.carInfos:  # make obejcts
            self.rectObjects.append(
                Rectangle(each[0], int(each[1]), int(each[2]), int(each[3])))

    def gameOver(self):  # if game is won
        # checks if starting coordinate of first car is at the winning position or not
        if self.rectObjects[0].startX == 320:
            messagebox.showinfo(
                'Congratulations!', 'You have completed the game!\nYou did it in %d moves!' % self.turns)  # victory popup
            self.inGame = False  # cut the loop


N = 6
EMPTY_SPACE = '_'
ICE_CREAM_TRUCK = 'A'
START_ROW = 2
PLIES = {}

class GenerateGame():

    def get_board():
        # Uppercase is horizontal, lowercase is vertical.
        board = [[EMPTY_SPACE] * 6 for _ in range(N)]
        # Initialize the ice cream truck in a random column.
        start_col = random.randrange(N - 2)
        board[START_ROW][start_col] = board[START_ROW][start_col + 1] = ICE_CREAM_TRUCK

        # Add more cars.
        num_attempts = 0
        for i in range(random.randrange(6, 10)):
            car_len = random.randrange(2, 4)
            while True:
                vertical = random.randrange(2) == 0
                r = random.randrange(N - (car_len - 1) * int(vertical))
                c = random.randrange(N - (car_len - 1) * int(not vertical))
                is_clear = True
                for j in range(car_len):
                    if board[r + j * int(vertical)][c + j * int(not vertical)] != EMPTY_SPACE:
                        is_clear = False
                        break

                if is_clear:
                    car_char = chr(ord('b' if vertical else 'B') + i)
                    for j in range(car_len):
                        board[r + j * int(vertical)][c + j *
                                                    int(not vertical)] = car_char
                    break

                num_attempts += 1
                if num_attempts > 1000:
                    # We have enough cars anyway.
                    break

        return board


    def board_str(board):
        return '\n'.join(' '.join(_) for _ in board)


    def copy_board(board):
        return [_[:] for _ in board]


    def is_solved(board):
        # Find any obstacles between the ice cream truck and the right edge.
        for i in range(N - 1, -1, -1):
            char_i = board[START_ROW][i]
            if char_i == EMPTY_SPACE:
                continue
            elif char_i == ICE_CREAM_TRUCK:
                return True
            else:
                return False

        return True


    def get_next_states(board):
        processed_chars_set = set([EMPTY_SPACE])
        next_states = []
        for r in range(N):
            for c in range(N):
                char = board[r][c]
                if char not in processed_chars_set:
                    processed_chars_set.add(char)
                    delta_r = 0
                    delta_c = 0
                    is_vertical = not char.isupper()
                    if is_vertical:
                        delta_r = 1
                    else:
                        delta_c = 1

                    # Find the extrema
                    min_r, max_r = r, r
                    min_c, max_c = c, c
                    while min_r - delta_r >= 0 and min_c - delta_c >= 0 and board[min_r - delta_r][min_c - delta_c] == char:
                        min_r -= delta_r
                        min_c -= delta_c

                    while max_r + delta_r < N and max_c + delta_c < N and board[max_r + delta_r][max_c + delta_c] == char:
                        max_r += delta_r
                        max_c += delta_c

                    if min_r - delta_r >= 0 and min_c - delta_c >= 0 and board[min_r - delta_r][min_c - delta_c] == EMPTY_SPACE:
                        next_state = GenerateGame.copy_board(board)
                        next_state[min_r - delta_r][min_c - delta_c] = char
                        next_state[max_r][max_c] = EMPTY_SPACE
                        next_states.append(next_state)

                    if max_r + delta_r < N and max_c + delta_c < N and board[max_r + delta_r][max_c + delta_c] == EMPTY_SPACE:
                        next_state = GenerateGame.copy_board(board)
                        next_state[min_r][min_c] = EMPTY_SPACE
                        next_state[max_r + delta_r][max_c + delta_c] = char
                        next_states.append(next_state)

        return next_states




    def search(board):
        queue = [(0, [board])]
        board_hash_set = set()

        while queue:
            ply, path = queue.pop(0)
            if ply not in PLIES:
                PLIES[ply] = 1
            else:
                PLIES[ply] += 1

            if GenerateGame.is_solved(path[-1]):
                return path

            for next_state in GenerateGame.get_next_states(path[-1]):
                if GenerateGame.board_str(next_state) not in board_hash_set:
                    board_hash_set.add(GenerateGame.board_str(next_state))
                    queue.append((ply + 1, path + [next_state]))

        return []


    def make_level_txt(board):
        letter = ['A', '_']
        blocks = []
        for i in range(6):
            if board[2][i] == 'A':
                blocks.append(['h', 2, 2, i])
                break

        for i in range(6):
            length = 0
            for j in range(6):
                if board[i][j] not in letter:
                    if board[i][j].isupper():
                        if board[i][j] == board[i][j + 1]:
                            if j + 2 < 6 and board[i][j] == board[i][j + 2]:
                                length = 3
                            else:
                                length = 2
                            letter.append(board[i][j])
                            blocks.append(['h', length, i, j])

                    else:
                        if board[i][j] == board[i + 1][j]:
                            if i + 2 < 6 and board[i][j] == board[i + 2][j]:
                                length = 3
                            else:
                                length = 2
                            letter.append(board[i][j])
                            blocks.append(['v', length, i, j])

        out = open('game0.txt', 'w')
        for i in blocks:
            out.write('{}, {}, {}, {}\n'.format(i[0], i[1], i[2], i[3]))
            print(i)


    def play():
        while True:
            board = GenerateGame.get_board()
            path = GenerateGame.search(board)
            # print('Solved length: {}'.format(len(path)))
            # print(PLIES)
            if len(path) >= 15:
                GenerateGame.make_level_txt(path[0])
                # for i in path[0]:
                #     print(i)
                print('\n\n'.join(GenerateGame.board_str(_) for _ in path))
                RushHour()
                break

# rushHour() #initialisre
