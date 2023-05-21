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
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+25 <= self.mouse[1] <= height/2+75:
                    new_state = Menu(self.game)
                    new_state.enter_state()

    def render(self, display):
        # display.fill((255,0,255))
        display.blit(self.game.bg,[0,0])
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        self.game.draw_text(display, "Traffic Jam Puzzle", (200,200,200), width/2+3, height/2-100+3, "head")
        self.game.draw_text(display, "Traffic Jam Puzzle", (200,200,200), width/2+3, height/2-100-3, "head")
        self.game.draw_text(display, "Traffic Jam Puzzle", (200,200,200), width/2-3, height/2-100+3, "head")
        self.game.draw_text(display, "Traffic Jam Puzzle", (200,200,200), width/2-3, height/2-100-3, "head")
        self.game.draw_text(display, "Traffic Jam Puzzle", (0,0,0), width/2, height/2-100, "head")
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+25 <= self.mouse[1] <= height/2+75:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.game.draw_text(display, "Start", (0,0,0), width/2+2, height/2+50+2, "head")
            self.game.draw_text(display, "Start", (0,0,0), width/2+2, height/2+50-2, "head")
            self.game.draw_text(display, "Start", (0,0,0), width/2-2, height/2+50+2, "head")
            self.game.draw_text(display, "Start", (0,0,0), width/2-2, height/2+50-2, "head")
            self.game.draw_text(display, "Start", (0,200,0), width/2, height/2+50, "head")
        else:
            pygame.mouse.set_cursor()
            self.game.draw_text(display, "Start", (200,200,200), width/2+2, height/2+50+2, "head")
            self.game.draw_text(display, "Start", (200,200,200), width/2+2, height/2+50-2, "head")
            self.game.draw_text(display, "Start", (200,200,200), width/2-2, height/2+50+2, "head")
            self.game.draw_text(display, "Start", (200,200,200), width/2-2, height/2+50-2, "head")
            self.game.draw_text(display, "Start", (0,0,0), width/2, height/2+50, "head")