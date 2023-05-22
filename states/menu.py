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
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # go to play
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
                    # jika belum ada level yang dibuat, buat level pertama
                    if(self.game.numlevel == 0):
                        self.game.newLevel()
                    new_state = Level(self.game)
                    new_state.enter_state()
                # go to help state
                elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
                    new_state = Help(self.game)
                    new_state.enter_state()
                # quit game
                elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
                    self.game.stop()

    def render(self, display):
        # display.fill((255,0,255))
        display.blit(self.game.bg,[0,0])
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        pressed = False
        playColor = (0,0,0)
        helpColor = (0,0,0)
        quitColor = (0,0,0)

        # kursor berada di tombol play
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
            playColor = (0,200,0)
            pressed = True
        # kursor berada di tombol help
        elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
            helpColor = (0,200,0)
            pressed = True
        # kursor berada di tombol quit
        elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
            quitColor = (0,200,0)
            pressed = True

        # jika ada tombol yang ditunjuk
        if pressed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()

        self.game.draw_text(display, "Main Menu", (0,0,0), width/2, height/2-200, "head")
        self.game.draw_text(display, "Play", playColor, width/2, height/2-75, "subhead")
        self.game.draw_text(display, "Help", helpColor, width/2, height/2+25, "subhead")
        self.game.draw_text(display, "Quit", quitColor, width/2, height/2+125, "subhead")