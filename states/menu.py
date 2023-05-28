# state menu menu
# berisi tombol play, help, dan back
import pygame
from states.state import State
from states.help import Help
from states.level import Level

class Menu(State):
    def __init__(self, game):
        pygame.init()        
        State.__init__(self, game)

    def get_events(self):
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # jika pemain ingin keluar, panggil method quit
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Jika menekan tombol play
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
                    # jika belum ada level yang dibuat, buat level pertama
                    if(self.game.numlevel == 0):
                        self.game.newLevel()
                    new_state = Level(self.game)
                    new_state.enter_state()
                # Jika menekan tombol help
                elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
                    new_state = Help(self.game)
                    new_state.enter_state()
                # Jika menekan tombol quit
                elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
                    self.game.stop()

    def render(self, display):
        display.blit(self.game.bg,[0,0])    # masukkan background 
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        pressed = False         # flag penanda terdapat tombol yang ditunjuk mouse
        playColor = (0,0,0)     # warna tombol play
        helpColor = (0,0,0)     # warna tombol help
        quitColor = (0,0,0)     # warna tombol quit

        # cek apakah mouse menunjuk tombol play
        # jika iya ubah pressed ke true
        # ubah warna tombol play ke hijau
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
            playColor = (0,200,0)
            pressed = True
        # cek apakah mouse menunjuk tombol help
        # jika iya ubah pressed ke true
        # ubah warna tombol help ke hijau
        elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
            helpColor = (0,200,0)
            pressed = True
        # cek apakah mouse menunjuk tombol quit
        # jika iya ubah pressed ke true
        # ubah warna tombol quit ke hijau
        elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
            quitColor = (0,200,0)
            pressed = True

        # jika ada tombol yang ditunjuk, ubah cursor
        if pressed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()

        # gambar tiap tombol dan text
        self.game.draw_text(display, "Main Menu", (0,0,0), width/2, height/2-200, "head")
        self.game.draw_text(display, "Play", playColor, width/2, height/2-75, "subhead")
        self.game.draw_text(display, "Help", helpColor, width/2, height/2+25, "subhead")
        self.game.draw_text(display, "Quit", quitColor, width/2, height/2+125, "subhead")