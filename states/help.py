# state menu help
# menampilkan cara bermain
import pygame
from states.state import State


class Help(State):
    def __init__(self, game):
        pygame.init()
        self.mouse = pygame.mouse.get_pos()
        State.__init__(self, game)

    # method untuk mendapatkan event
    def get_events(self):
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # jika pemain ingin keluar, panggil method stop pada game
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # jika pemain menekan tombol back, panggil method back pada game
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+225 <= self.mouse[1] <= height/2+275:
                    self.game.back()

    # method untuk merender objek yang diperlukan
    def render(self, display):
        display.blit(self.game.bg, [0, 0])    # masukkan background
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        pressed = False                       # penanda terdapat tombol yang ditunjuk mouse
        backColor = (0, 0, 0)                 # warna tombol back

        # cek apakah mouse menunjuk tombol back
        # jika iya ubah pressed ke true
        # ubah warna tombol back ke hijau
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+225 <= self.mouse[1] <= height/2+275:
            pressed = True
            backColor = (0, 200, 0)
        else:
            pressed = False

        # render text help
        self.game.draw_text(display, "Help", (0, 0, 0),
                            width/2, height/2-250, "head")

        # membuat kotak untuk text help
        pygame.draw.rect(display, (250, 250, 250),
                         pygame.Rect(50, 150, 700, 300))
        
        # membaca text pada asset, kemudian render tiap barisnya
        i = 0
        file = open('./assets/text/help.txt', 'r')
        Lines = file.read().splitlines()
        for line in Lines:
            self.game.draw_text(display, line, (0, 0, 0),
                                width/2, height/2-125+i, "text")
            i += 20

        # render tombol back
        self.game.draw_text(display, "Back", backColor,
                            width/2, height/2+250, "subhead")

        # jika mouse menunjuk tombol
        if pressed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()
