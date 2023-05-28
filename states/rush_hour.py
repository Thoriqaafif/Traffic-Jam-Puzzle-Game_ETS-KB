# state menu game
# berisi level, tombol back
# tombol hint, dan papan permainan
import pygame
import random
import sys
import math
from tkinter import *
from tkinter import messagebox
from states.state import State

surfaceSize = 420               # game surface size
minx = (800-surfaceSize)/2      # x-coordinates starts of game box
miny = (600-surfaceSize)/2+50   # y-coordinates starts of game box

# tiap objek dianggap persegi panjang
# untuk menentukan posisi, orientasi, kode, dan ukurannya
class Rectangle:
    def __init__(self, orientation, size, row, column, kode):
        perSq = 70      # tiap kotak berukuran 70x70
        self.startX = column * perSq    # koordinat x awal
        self.startY = row * perSq       # koordinat y awal
        self.orientation = orientation  # arah gerak objek
        self.size = size                # ukuran objek
        self.becak = False              # flag yang menandakan becak atau tidak
        self.kode = kode                # kode objek pada matriks
        
        if self.orientation == "h": # untuk objel horizontal
            length = perSq * size       # panjang objek
            self.extendX = length       # besar objek memanjang secara horizontal
            self.extendY = perSq        # besar objek memanjang secara vertikal
            self.startLimitX = 0        # koordinat x awal dimana objek dapat diletakkan
            self.startLimitY = self.startY # koordinat y awal dimana objek dapat diletakkan
            self.endLimitX = surfaceSize - length + perSq # koordinat x akhir dimana objek dapat diletakkan
            self.endLimitY = self.startY + self.extendY # koordinat y akhir dimana objek dapat diletakkan
            
        else: # untuk objek vertikal
            length = perSq * size       # panjang objek
            self.extendX = perSq        # besar objek memanjang secara horizontal
            self.extendY = length       # besar objek memanjang secara vertikal
            self.startLimitX = self.startX  # koordinat x awal dimana objek dapat diletakkan
            self.startLimitY = 0        # koordinat y awal dimana objek dapat diletakkan
            self.endLimitX = self.startX + self.extendX # koordinat x akhir dimana objek dapat diletakkan
            self.endLimitY = surfaceSize - length + perSq # koordinat y akhir dimana objek dapat diletakkan

        # jika objek berada pada baris 2
        # dan berarah horizontal
        # maka objek adalah becak
        if row == 2 and orientation == 'h': #if it is the first car (car needed to get across)
            self.becak=True

        self.currentX = self.startX + 0 # koordinat x objek saat ini
        self.currentY = self.startY + 0 # koordinat y objek saat ini

        self.rectDrag = False # flag yang menandakan apakah objek sedang dipindahkan
        self.rect = pygame.Rect(self.startX, self.startY, self.extendX, self.extendY) # buat object rectangle

# kelas utama untuk menjalankan puzzle
class RushHour(State):

    def __init__(self,game,level):
        State.__init__(self,game)

        # load puzzle dari file txt
        self.loadGame(level)
        self.makeRectangles()
        self.turns = 0
        self.level=level

        # load hint dari file txt
        self.path = self.loadHint(level)

        pygame.init()  # run pygame

        self.start = True   # flag yang menunjukkan game baru dimulai

    def get_events(self):
        self.ev = pygame.event.poll()
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT

        # jika pemain ingin keluar, panggil method quit
        if self.ev.type == pygame.QUIT:  # if window exited
            self.game.stop()

        elif self.ev.type == pygame.MOUSEBUTTONDOWN: # jika pemain menekan cursor
            self.mouseX, self.mouseY = self.ev.pos
            # cek apakah pemain menekan back
            if 50 <= self.mouseX <= 150 and 25 <= self.mouseY <= 75:
                self.game.back()
            # cek apakah pemain menekan hint
            elif width-150 <= self.mouseX <= width-50 and 25 <= self.mouseY <= 75:
                # panggil method hint
                board=self.game.hint(self.board)
                # jika tidak ada langkah selanjutnya, game telah selesai
                if(board == None):
                    self.rectObjects[0].startX = 280
                    self.rectObjects[0].startY = 140
                    self.rectObjects[0].rect = pygame.Rect(280, 140, self.rectObjects[0].extendX, self.rectObjects[0].extendY)
                # ubah board sekarang dengan board yang didapat dari hint
                # evaluasi objek rect nya sesuai dengan board baru
                else:
                    self.board = board
                    self.convertBoard()
                
                self.turns+=1   # tambah turns permainan
            # cek apakah pemain menggerakkan blok
            else:
                self.clickObject()

        elif self.ev.type == pygame.MOUSEBUTTONUP:  # jika pemain melepas kursor
            self.unclickObject()

        elif self.ev.type == pygame.MOUSEMOTION:  # jika pemain menggerakkan mouse
            self.objectMidAir()

        # jika pemain baru masuk, beri pesan pembuka
        if (self.start):
            messagebox.showinfo('Welcome!', 'Rush Hour\nGet the red car to the end.\n Click and drag to control the cars.')
            self.start = False

        # cek apakah game sudah berhasil diselesaikan
        self.gameOver()

    def render(self, surface):
        surface.blit(self.game.bg,[0,0])    # beri background
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        white=(250,250,250)
        self.mouse = pygame.mouse.get_pos()

        # menggambar kotak tempat permainan
        for i in range(6):
            for j in range(6):
                surface.blit(self.game.tanah,[minx+j*70,miny+i*70])
        for x in range(len(self.rectObjects)):  # untuk tiap objek
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
                # jika blok ukuran 3, gambar car1
                elif size==3:
                    if orientation == 'h':
                        surface.blit(self.game.car1H,[startX+5, startY])
                    else:
                        surface.blit(self.game.car1V,[startX, startY+5])
                
        pressed = False     # flag penanda terdapat tombol yang ditunjuk mouse
        backColor = (0,0,0) # warna tombol back
        hintColor = (0,0,0) # warna tombol hint

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

        # gambar tiap tombol dan text
        self.game.draw_text(surface, "back", backColor, 100, 50, "subhead")
        self.game.draw_text(surface, str(self.level), (0,0,0), width/2, 50, "head")
        self.game.draw_text(surface, "hint", hintColor, width - 100, 50, "subhead")

    def clickObject(self):  # ketika pemain mengeklik papan permainan
        for x in range(len(self.rectObjects)):  # untuk tiap objek
            startX = self.rectObjects[x].rect.x+minx
            startY = self.rectObjects[x].rect.y+miny
            w = self.rectObjects[x].rect.width
            h = self.rectObjects[x].rect.height
            objectRect=pygame.Rect(startX,startY,w,h)

            # jika koordinat yang diklik terdapat objek
            if objectRect.collidepoint(self.ev.pos):
                self.rectObjects[x].rectDrag = True  # buat objek di udara
                self.mouseX, self.mouseY = self.ev.pos  # mendapat posisi mouse saat ini
                # mendapat selisih koordinat mouse dengan objek
                self.offsetX = self.rectObjects[x].rect.x - self.mouseX
                self.offsetY = self.rectObjects[x].rect.y - self.mouseY
                break  # stop the loop

    def objectMidAir(self):  # ketika objek sedang ditarik
        for x in range(len(self.rectObjects)):  # untuk tiap objek
            if self.rectObjects[x].rectDrag:  # jika objek berada di udara
                self.mouseX, self.mouseY = self.ev.pos  # mendapat posisi mouse saat ini
                self.rectObjects[x].rect.x = self.mouseX + \
                    self.offsetX  # mendapat koordinat objek di udara
                self.rectObjects[x].rect.y = self.mouseY + self.offsetY

    def unclickObject(self):  # ketika objek diletakkan
        for x in range(len(self.rectObjects)): # untuk tiap objek
            if self.rectObjects[x].rectDrag: # jika objek berada di udara

                perSq = 70 # satu kotak berukuran 70x70
                # dapatkan baris dan kolom objek
                makeshiftColumn, makeshiftRow = self.rectObjects[x].rect.x / perSq, self.rectObjects[x].rect.y / perSq
                decimalColumn, decimalRow = makeshiftColumn % 1, makeshiftRow % 1

                # melakukan pembulatan berdasarkan nilai desimalnya
                # jika desimal lebih dari sama dengan 0.5 lakukan pembulatan ke atas
                # jika desimal kurang dari 0.5 lakukan pembulatan ke bawah
                if decimalColumn >= 0.5:
                    jumpX = math.ceil(makeshiftColumn) * perSq
                else:
                    jumpX = math.floor(makeshiftColumn) * perSq   
                if decimalRow >= 0.5:
                    jumpY = math.ceil(makeshiftRow) * perSq
                else:
                    jumpY = math.floor(makeshiftRow) * perSq

                # buat list sementara tanpa objek yang dipindah sebagai perbandingan
                temporaryRectangles = self.rectObjects * 1
                temporaryRectangles.remove(self.rectObjects[x])

                # mendapat koordinat tengah objek
                middleY = (self.rectObjects[x].startY + self.rectObjects[x].extendY + self.rectObjects[x].startY) / 2
                middleX = (self.rectObjects[x].startX + self.rectObjects[x].extendX + self.rectObjects[x].startX) / 2
                moveAllowed = True # flag yang menandakan pergerakan dibolehkan

                # mendapat kotak awal dan akhir untuk mengecek collision
                if self.rectObjects[x].orientation == "h":
                    countStart = int(self.rectObjects[x].currentX /perSq) 
                    countEnd = int(jumpX / perSq) 
                    if countStart > countEnd: # jika awal lebih besar, maka tukar
                        countStart, countEnd = countEnd, countStart    
                else: # untuk vertikal, tukar X dan Y
                    countStart = int(self.rectObjects[x].currentY /perSq)
                    countEnd = int(jumpY / perSq)
                    if countStart > countEnd: # jika awal lebih besar, maka tukar
                        countStart, countEnd = countEnd, countStart

                # bergantung ukuran objek dimana kita harus mengecek collision
                if self.rectObjects[x].size == 2:
                    divisor = 2
                else:
                    divisor = 3
                

                for y in range(len(temporaryRectangles)): # untuk tiap objek
                    for z in range(countStart, countEnd+1): # untuk tiap objek yang ada pada pergerakan
                        if self.rectObjects[x].orientation == "h":
                            middleX = ((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor # mendapat nilai tengah baru
                            middleX2 = (((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor) * (divisor-1) # untuk objek ukuran 3
                            # mengecek apakah koordinat 'middle' berada di antara objek lain
                            if ((temporaryRectangles[y].startX <= middleX <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX)) or (temporaryRectangles[y].startX <= middleX2 <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX))) and (temporaryRectangles[y].startY <= middleY <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY)):
                                moveAllowed = False
                                # jika terdapat collision, maka pergerakan dibatalkan
                                break
                            else:
                                moveAllowed = True
                        else: # untuk bertikal, tukar x dan y                          
                            middleY = ((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor
                            middleY2 = (((z*perSq) + (((z+1)*perSq)+(((self.rectObjects[x].size-1)*perSq)))) / divisor) * (divisor-1)
                            if (temporaryRectangles[y].startX <= middleX <= (temporaryRectangles[y].extendX + temporaryRectangles[y].startX)) and ((temporaryRectangles[y].startY <= middleY <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY)) or (temporaryRectangles[y].startY <= middleY2 <= (temporaryRectangles[y].extendY + temporaryRectangles[y].startY))):
                                moveAllowed = False
                                break
                            else:
                                moveAllowed = True
                                
                    if moveAllowed == False:
                            break
                    
                # cek apakah koordinat baru berada pada limit atau tidak
                if (self.rectObjects[x].startLimitX <= jumpX < self.rectObjects[x].endLimitX) and (self.rectObjects[x].startLimitY <= jumpY < self.rectObjects[x].endLimitY) and moveAllowed:
                    row0=self.rectObjects[x].startY//perSq
                    col0=self.rectObjects[x].startX//perSq
                    row=jumpY//perSq
                    col=jumpX//perSq
                    size=self.rectObjects[x].size
                    kode = self.board[row0][col0]
                    # jika horizontal, update kolom sebelahnya
                    if row0==row and col0 != col:
                        for idx in range(size):
                            self.board[row][col0+idx]='_'
                        for idx in range(size):
                            self.board[row][col+idx]=kode
                    # jika vertikal, update baris sebelahnya
                    if col0==col and row0 != row:
                        for idx in range(size):
                            self.board[row0+idx][col]='_'
                        for idx in range(size):
                            self.board[row+idx][col]=kode

                    # update atribut yang dibutuhkan
                    self.rectObjects[x].rect = pygame.Rect(jumpX, jumpY, self.rectObjects[x].extendX, self.rectObjects[x].extendY)
                    self.rectObjects[x].currentX = jumpX
                    self.rectObjects[x].currentY = jumpY
                    self.rectObjects[x].startX = jumpX
                    self.rectObjects[x].startY = jumpY
                    self.rectObjects[x].rectDrag = False
                    self.turns += 1 

                # jika tidak sesuai, pergerakan dibatalkan
                # kemabilkan objek ke lokasi semula
                # beri pesan error
                else: 
                    self.rectObjects[x].rect = pygame.Rect(self.rectObjects[x].currentX, self.rectObjects[x].currentY, self.rectObjects[x].extendX, self.rectObjects[x].extendY)
                    self.rectObjects[x].rectDrag = False
                    messagebox.showwarning('Error','You cannot make that move.')

    # method untuk membaca level dari file txt
    def loadGame(self, level):
        self.carInfos = []  # list informasi objek
        filename = "./assets/level/game"+str(level)+".txt"
        file = open(filename, 'r')  # buka file
        lines = file.readlines()
        self.board = [['_'] * 6 for _ in range(6)]  # membuat papan permainan

        for x in range(len(lines)):
            # untuk tiap baris, hapus newline
            lines[x] = lines[x][:-1]

        i=0
        for line in lines:
            # memberi kode untuk tiap objek
            kode = chr(ord('A')+i)
            # memasukkan tiap data ke tiap variabel
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

    # method untuk membaca hint dari file txt
    def loadHint(self, level):  # membaca file
        hints = []  # list informasi objek
        filename = "./assets/hint/game"+str(self.game.numlevel)+".txt"
        file = open(filename, 'r')  # buka file
        lines = file.readlines() 

        for x in range(len(lines)):
            # untuk tiap baris, hapus newline
            lines[x] = lines[x][:-1]

        for line in lines:
            # memasukkan data pada list hints
            hints.append(line)
        return hints

    # method untuk membuat objek rectangle
    def makeRectangles(self):
        self.rectObjects = []
        for each in self.carInfos:
            row = int(each[2])
            col = int(each[3])
            kode = self.board[row][col]
            self.rectObjects.append(
                Rectangle(each[0], int(each[1]), row, col,kode))
    
    # method untuk mengevaluasi tiap objek dengan board
    def convertBoard(self):
        finish = set()
        for i in range(6):
            for j in range(6):
                kode = self.board[i][j]
                for obj in self.rectObjects:
                    if(obj.kode == kode and kode not in finish):
                        obj.rect = pygame.Rect(70*j, 70*i, obj.extendX, obj.extendY)
                        obj.currentX = 70*j
                        obj.currentY = 70*i
                        obj.startX = 70*j
                        obj.startY = 70*i
                        obj.rectDrag = False
                finish.add(kode)

    # cek apakah game telah diselesaikan
    def gameOver(self):
        # game dimenangkan jika objek utama berada di kolom ke-4
        # atau koordinat berada pada (panjang papan - 2 kotak (140))
        if self.rectObjects[0].startX == surfaceSize-140:
            # beri pesan kemenangan dengan jumlah moves yang dilakukan
            messagebox.showinfo(
                'Congratulations!', 'You have completed the game!\nYou did it in %d moves!' % self.turns) 
            if(self.level==self.game.numlevel):
                self.game.newLevel()    # buat level baru
            self.game.back()        # pop state sekarang
            # buat state RushHour level selanjutnya
            new_state = RushHour(self.game,self.level+1)
            new_state.enter_state()