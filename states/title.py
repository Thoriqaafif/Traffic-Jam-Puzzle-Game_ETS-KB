import pygame
from states.state import State
from states.menu import Menu

class Title(State):
    def __init__(self, game):
        pygame.init()
        self.mouse = pygame.mouse.get_pos()        
        State.__init__(self, game)

    def get_events(self):
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # jika user melakukan quit game, stop game
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # jika mouse menekan start, pindah ke menu
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-25 <= self.mouse[1] <= height/2+25:
                    new_state = Menu(self.game)
                    new_state.enter_state()

    def render(self, display):
        # display.fill((255,0,255))
        display.blit(self.game.bg,[0,0])
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        pressed = False
        startColor = (0,0,0)

        # jika mouse menunjuk start, ubah warna ke hijau
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-25 <= self.mouse[1] <= height/2+25:
            startColor = (0,200,0)
            pressed = True
        else:
            pressed = False

        # jika ada tombol yang ditunjuk
        if pressed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()

        # render the text
        self.game.draw_text(display, "Becak Terjebak", (0,0,0), width/2, height/2-125, "head")
        self.game.draw_text(display, "Start", startColor, width/2, height/2, "subhead")

        # gambar logo becak
        display.blit(self.game.becaklogo,[325,375])