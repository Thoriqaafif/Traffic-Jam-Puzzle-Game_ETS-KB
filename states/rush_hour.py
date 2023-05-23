# imports libraries
import pygame
import random
import sys
import math
from tkinter import *
from tkinter import messagebox
from states.state import State

Tk().wm_withdraw()  # to hide the main Tkinter window

surfaceSize = 420               # game surface size
minx = (800-surfaceSize)/2      # x-coordinates starts of game box
miny = (600-surfaceSize)/2+50   # y-coordinates starts of game box

# each of block is a rectangle block
class Rectangle:  # rectangle class (the car)

    def __init__(self, orientation, size, row, column, kode):
        perSq = 70 #one square is 80x80
        self.startX = column * perSq #starting x-coordinate
        self.startY = row * perSq #starting y-coordinate
        self.orientation = orientation
        self.size = size
        self.becak = False  # flag yang menandakan becak atau tidak
        self.kode = kode
        
        if self.orientation == "h": #for horizontal cars
            length = perSq * size
            self.extendX = length #How much the x-coordinate extends by
            self.extendY = perSq #How much the y-coordinate extends by
            self.colour = (0, 255, 0)
            self.startLimitX = 0 #Starting x coordinate of where the car can be positioned
            self.startLimitY = self.startY #Starting y coordinate of where the car can be positioned
            self.endLimitX = surfaceSize - length + perSq #Ending x coordinate of where the car can be positioned
            self.endLimitY = self.startY + self.extendY #Ending y coordinate of where the car can be positioned
            
        else: #same as above, but for vertical, so swap x and y
            length = perSq * size
            self.extendX = perSq
            self.extendY = length
            self.colour = (0, 0, 255)
            self.startLimitX = self.startX
            self.startLimitY = 0
            self.endLimitX = self.startX + self.extendX
            self.endLimitY = surfaceSize - length + perSq

        if row == 2 and orientation == 'h': #if it is the first car (car needed to get across)
            self.becak=True
            self.colour = (204, 0, 0) #make it its own different colour to differentiate

        self.currentX = self.startX + 0 #current x-coordinate of car
        self.currentY = self.startY + 0 #current y-coordinate of car

        self.rectDrag = False #boolean if the car is currently being dragged or not
        self.rect = pygame.Rect(self.startX, self.startY, self.extendX, self.extendY) #make rectangle object


class RushHour(State):  # main game class

    def __init__(self,game,level):
        State.__init__(self,game)

        # self.board=translateLevel()
        self.loadGame(level)
        self.makeRectangles()
        self.turns = 0
        self.level=level
        self.path = self.loadHint(level)

        pygame.init()  # run pygame

        self.start = True

    def get_events(self):
        self.ev = pygame.event.poll()  # pygame events
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT

        if self.ev.type == pygame.QUIT:  # if window exited
            self.game.stop()

        elif self.ev.type == pygame.MOUSEBUTTONDOWN:  # if the window has been left-clicked
            self.mouseX, self.mouseY = self.ev.pos
            # cek apakah pemain menekan back
            if 50 <= self.mouseX <= 150 and 25 <= self.mouseY <= 75:
                self.game.back()
            # cek apakah pemain menekan hint
            elif width-150 <= self.mouseX <= width-50 and 25 <= self.mouseY <= 75:
                count = 0
                for line in self.path:
                    print(line)
                    count += 1
                print("Jumlah path: {}".format(count // 7))
                self.turns+=1
                board=self.game.hint(self.board)
                if(board == None):
                    self.rectObjects[0].startX = 280
                    self.rectObjects[0].startY = 140
                    self.rectObjects[0].rect = pygame.Rect(280, 140, self.rectObjects[0].extendX, self.rectObjects[0].extendY)
                else:
                    self.board = board
                    self.convertBoard()
            # cek apakah pemain menggerakkan blok
            else:
                self.clickObject()

        elif self.ev.type == pygame.MOUSEBUTTONUP:  # if the window has been released from the left-click
            self.unclickObject()

        elif self.ev.type == pygame.MOUSEMOTION:  # if the lect click is still being clicked
            self.objectMidAir()

        # jika pemain baru masuk, beri pesan pembuka
        if (self.start):
            messagebox.showinfo('Welcome!', 'Rush Hour\nGet the red car to the end.\n Click and drag to control the cars.')
            self.start = False

        # cek apakah game sudah berhasil diselesaikan
        self.gameOver()

    def render(self, surface):
        # surface.fill((255, 0, 255))
        surface.blit(self.game.bg,[0,0])
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        white=(250,250,250)
        self.mouse = pygame.mouse.get_pos()

        # menggambar kotak tempat permainan
        for i in range(6):
            for j in range(6):
                surface.blit(self.game.tanah,[minx+j*70,miny+i*70])
        # pygame.draw.rect(surface,white,pygame.Rect(minx,miny,surfaceSize,surfaceSize))
        for x in range(len(self.rectObjects)):  # for each rectangle
                # surface.blit(self.game.car,[self.rectObjects[x].rect.x,self.rectObjects[x].rect.y])
                # colour fill the rectangles
                startX = self.rectObjects[x].rect.x+minx
                startY = self.rectObjects[x].rect.y+miny
                orientation = self.rectObjects[x].orientation
                size = self.rectObjects[x].size
                w = self.rectObjects[x].rect.width
                h = self.rectObjects[x].rect.height
                # jika blok utama, gambar becak
                if self.rectObjects[x].becak:
                    surface.blit(self.game.becak,[startX+20, startY])
                # jika blok ukuran 2, gambar car2
                elif size==2:
                    if orientation == 'h':
                        surface.blit(self.game.car2H,[startX, startY])
                    else:
                        surface.blit(self.game.car2V,[startX, startY])
                    # surface.fill(self.rectObjects[x].colour, pygame.Rect(startX,startY,w,h))
                    # draw rectangles, with black borders
                    # pygame.draw.rect(surface, (0, 0, 0),
                    #              pygame.Rect(startX,startY,w,h), 5)
                # jika blok ukuran 3, gambar car1
                elif size==3:
                    if orientation == 'h':
                        surface.blit(self.game.car1H,[startX+5, startY])
                    else:
                        surface.blit(self.game.car1V,[startX, startY+5])
                
        pressed = False
        backColor = (0,0,0)
        hintColor = (0,0,0)

        # kursor berada di tombol back
        if 50 <= self.mouse[0] <= 150 and 25 <= self.mouse[1] <= 75:
            backColor = (0,200,0)
            pressed = True
        # kursor berada di tombol hint
        elif width-150 <= self.mouse[0] <= width-50 and 25 <= self.mouse[1] <= 75:
            hintColor = (0,200,0)
            pressed = True

        # jika ada tombol yang ditunjuk
        if pressed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()

        self.game.draw_text(surface, "back", backColor, 100, 50, "subhead")
        self.game.draw_text(surface, str(self.level), (0,0,0), width/2, 50, "head")
        self.game.draw_text(surface, "hint", hintColor, width - 100, 50, "subhead")

    def clickObject(self):  # when the window is clicked
        for x in range(len(self.rectObjects)):  # for every object
            startX = self.rectObjects[x].rect.x+minx
            startY = self.rectObjects[x].rect.y+miny
            w = self.rectObjects[x].rect.width
            h = self.rectObjects[x].rect.height
            objectRect=pygame.Rect(startX,startY,w,h)
            # if the coordinates of the click is within a rectangle
            if objectRect.collidepoint(self.ev.pos):
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
        for x in range(len(self.rectObjects)): #for each rectangle
            if self.rectObjects[x].rectDrag: #if the rectangle is in the air

                perSq = 70 #one square is 80x80
                #get the 'row and column' of where the rectangle is
                makeshiftColumn, makeshiftRow = self.rectObjects[x].rect.x / perSq, self.rectObjects[x].rect.y / perSq
                decimalColumn, decimalRow = makeshiftColumn % 1, makeshiftRow % 1

                #depending on decimal part, whether to round up or round down
                #math.ceil will get rid of decimal part and round up
                #math.floor will get rid of decimal part and round down
                if decimalColumn >= 0.5:
                    jumpX = math.ceil(makeshiftColumn) * perSq
                else:
                    jumpX = math.floor(makeshiftColumn) * perSq   
                if decimalRow >= 0.5:
                    jumpY = math.ceil(makeshiftRow) * perSq
                else:
                    jumpY = math.floor(makeshiftRow) * perSq
                #jump is the proposed coordinate following multiples of 80
                #say the midair x-coordinate is something like 146, the jumpX will be 160

                #make a temporary list without the rectangle being held for rectangle comparison
                temporaryRectangles = self.rectObjects * 1
                temporaryRectangles.remove(self.rectObjects[x])

                #get the coordinates in the middle of the rectangle
                middleY = (self.rectObjects[x].startY + self.rectObjects[x].extendY + self.rectObjects[x].startY) / 2
                middleX = (self.rectObjects[x].startX + self.rectObjects[x].extendX + self.rectObjects[x].startX) / 2
                moveAllowed = True #boolean for allowing the move

                if self.rectObjects[x].orientation == "h":
                    countStart = int(self.rectObjects[x].currentX /perSq) #get the starting square that is needed to be checked for collisions
                    countEnd = int(jumpX / perSq) #get the last square that is needed to be checked for collision
                    if countStart > countEnd: #if start is bigger then swap
                        countStart, countEnd = countEnd, countStart
                    
                else: #same but just for vertical, swap X and Y
                    countStart = int(self.rectObjects[x].currentY /perSq)
                    countEnd = int(jumpY / perSq)
                    if countStart > countEnd:
                        countStart, countEnd = countEnd, countStart

                #depending on size of car, where to check for collision
                #okay i kind of lied about it being the 'middle', because for size 3 car
                #it would check 1/3 and 2/3 of the rectangle
                if self.rectObjects[x].size == 2:
                    divisor = 2

                else:
                    divisor = 3
                

                for y in range(len(temporaryRectangles)): #for each rectangle
                    for z in range(countStart, countEnd+1): #for each square between the move
                        if self.rectObjects[x].orientation == "h":
                            middleX = ((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor #get the new middle coordinate
                            middleX2 = (((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor) * (divisor-1) #for size 3 cars
                            #this monster if statement checks whether or not the 'middle' coordinate is between the coordinates of another rectangle or not
                            if ((temporaryRectangles[y].startX <= middleX <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX)) or (temporaryRectangles[y].startX <= middleX2 <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX))) and (temporaryRectangles[y].startY <= middleY <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY)):
                                moveAllowed = False
                                #if there is a collision then it cannot move
                                break
                            else:
                                moveAllowed = True
                        else: #for vertical, same as above, just swap X and Y                            
                            middleY = ((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor
                            middleY2 = (((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor) * (divisor-1)
                            if (temporaryRectangles[y].startX <= middleX <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX)) and ((temporaryRectangles[y].startY <= middleY <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY)) or (temporaryRectangles[y].startY <= middleY2 <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY))):
                                moveAllowed = False
                                break
                            else:
                                moveAllowed = True
                                
                    if moveAllowed == False:
                            break
                #this semi-monster if statement checks whether the new proposed coordinates of the rectangle is within the limits or not
                #and also checks for collision
                if (self.rectObjects[x].startLimitX <= jumpX < self.rectObjects[x].endLimitX) and (self.rectObjects[x].startLimitY <= jumpY < self.rectObjects[x].endLimitY) and moveAllowed:
                    row0=self.rectObjects[x].startY//perSq
                    col0=self.rectObjects[x].startX//perSq
                    row=jumpY//perSq
                    col=jumpX//perSq
                    size=self.rectObjects[x].size
                    kode = self.board[row0][col0]
                    # jika horizontal
                    if row0==row and col0 != col:
                        for idx in range(size):
                            self.board[row][col0+idx]='_'
                        for idx in range(size):
                            self.board[row][col+idx]=kode

                    # jika vertikal
                    if col0==col and row0 != row:
                        for idx in range(size):
                            self.board[row0+idx][col]='_'
                        for idx in range(size):
                            self.board[row+idx][col]=kode
                            
                    # print('')
                    # for line in self.board:
                    #     print(line)

                    #update the necessary attributes of the rectangle
                    self.rectObjects[x].rect = pygame.Rect(jumpX, jumpY, self.rectObjects[x].extendX, self.rectObjects[x].extendY)
                    self.rectObjects[x].currentX = jumpX
                    self.rectObjects[x].currentY = jumpY
                    self.rectObjects[x].startX = jumpX
                    self.rectObjects[x].startY = jumpY
                    self.rectObjects[x].rectDrag = False
                    self.turns += 1 

                else: #if it doesnt match
                    #put the rectangle back to where the user moved it from
                    self.rectObjects[x].rect = pygame.Rect(self.rectObjects[x].currentX, self.rectObjects[x].currentY, self.rectObjects[x].extendX, self.rectObjects[x].extendY)
                    self.rectObjects[x].rectDrag = False
                    messagebox.showwarning('Error','You cannot make that move.') #error message popup

    def loadGame(self, level):  # reading the file
        self.carInfos = []  # list of car information
        filename = "./assets/level/game"+str(level)+".txt"  # get 2nd file
        file = open(filename, 'r')  # open it
        lines = file.readlines()  # save the file to a list
        self.board = [['_'] * 6 for _ in range(6)]  # membuat papan permainan

        for x in range(len(lines)):
            # for each line, get rid of the \n that appears at the end
            lines[x] = lines[x][:-1]

        i=0
        for line in lines:
            # memberi kode untuk tiap objek
            kode = chr(ord('A')+i)
            # seperate each data to its own string and add to list
            carInfo=line.split(',')
            orientation=carInfo[0]
            size = int(carInfo[1])
            row = int(carInfo[2])
            col = int(carInfo[3])
            if orientation == 'h':
                kode = chr(ord('A')+i) # memberi kode
                for j in range(size):
                    self.board[row][col+j]=kode
            elif orientation == 'v':
                kode = chr(ord('b')+i) # memberi kode
                for j in range(size):
                    self.board[row+j][col]=kode
            self.carInfos.append(carInfo)
            i+=1

    def loadHint(self, level):  # reading the file
        hints = []  # list of car information
        filename = "./assets/hint/game"+str(self.game.numlevel)+".txt"  # get 2nd file
        file = open(filename, 'r')  # open it
        lines = file.readlines()  # save the file to a list

        for x in range(len(lines)):
            # for each line, get rid of the \n that appears at the end
            lines[x] = lines[x][:-1]

        for line in lines:
            # seperate each data to its own string and add to list
            hints.append(line)
        return hints

    def makeRectangles(self):  # make rectangle objects
        self.rectObjects = []  # list of rectangle objects
        for each in self.carInfos:  # make obejcts
            row = int(each[2])
            col = int(each[3])
            kode = self.board[row][col]
            self.rectObjects.append(
                Rectangle(each[0], int(each[1]), row, col,kode))
            
    def convertBoard(self):
        finish = set()
        for i in range(6):
            for j in range(6):
                kode = self.board[i][j]
                for obj in self.rectObjects:
                    if(obj.kode == kode and kode not in finish):
                        # print("huee")
                        obj.rect = pygame.Rect(70*j, 70*i, obj.extendX, obj.extendY)
                        # obj.rect.startX=70*j
                        # obj.rect.startY=70*i
                finish.add(kode)

    def gameOver(self):  # if game is won
        # checks if starting coordinate of first car is at the winning position or not
        if self.rectObjects[0].startX == surfaceSize-140:
            messagebox.showinfo(
                'Congratulations!', 'You have completed the game!\nYou did it in %d moves!' % self.turns)  # victory popup
            if(self.level==self.game.numlevel):
                self.game.newLevel()    # buat level baru
            self.game.back()        # pop state sekarang
            # buat state RushHour level selanjutnya
            new_state = RushHour(self.game,self.level+1)
            new_state.enter_state()