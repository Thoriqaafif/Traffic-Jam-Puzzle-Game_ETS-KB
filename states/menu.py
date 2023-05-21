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
        display.fill((255,0,255))
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        self.game.draw_text(display, "Main Menu", (0,0,0), width/2, height/2-200, "head")

        # kursor berada di tombol play
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.game.draw_text(display, "Play", (0,200,0), width/2, height/2-75, "head")   # hijau
            self.game.draw_text(display, "Help", (0,0,0), width/2, height/2+25, "head")
            self.game.draw_text(display, "Quit", (0,0,0), width/2, height/2+125, "head")

        # kursor berada di tombol help
        elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.game.draw_text(display, "Play", (0,0,0), width/2, height/2-75, "head")
            self.game.draw_text(display, "Help", (0,200,0), width/2, height/2+25, "head")   # hijau
            self.game.draw_text(display, "Quit", (0,0,0), width/2, height/2+125, "head")

        # kursor berada di tombol quit
        elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.game.draw_text(display, "Play", (0,0,0), width/2, height/2-75, "head")
            self.game.draw_text(display, "Help", (0,0,0), width/2, height/2+25, "head")
            self.game.draw_text(display, "Quit", (0,200,0), width/2, height/2+125, "head")  # hijau
        
        # kursor tidak berada di tombol
        else:
            pygame.mouse.set_cursor()
            self.game.draw_text(display, "Play", (0,0,0), width/2, height/2-75, "head")
            self.game.draw_text(display, "Help", (0,0,0), width/2, height/2+25, "head")
            self.game.draw_text(display, "Quit", (0,0,0), width/2, height/2+125, "head")