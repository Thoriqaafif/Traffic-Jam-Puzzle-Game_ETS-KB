import pygame
from states.state import State
from states.rush_hour import RushHour

class Level(State):
    def __init__(self, game):
        pygame.init()
        self.mouse = pygame.mouse.get_pos()        
        State.__init__(self, game)
        self.padding=100
        self.margin=100

    def get_events(self):
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.padding-25 <= self.mouse[0] <= self.padding+25 and self.padding-25 <= self.mouse[1] <= self.padding+25:
                    new_state=RushHour(self.game,1)
                    new_state.enter_state()

    def render(self, display):
        display.fill((255,0,255))
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()

        if self.padding-25 <= self.mouse[0] <= self.padding+25 and self.padding-25 <= self.mouse[1] <= self.padding+25:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.game.draw_text(display, "1", (0,200,0), self.padding, self.padding, "head")
        else:
            pygame.mouse.set_cursor()
            self.game.draw_text(display, "1", (0,0,0), self.padding, self.padding, "head")

        if self.padding+self.margin-25 <= self.mouse[0] <= self.padding+self.margin+25 and self.padding-25 <= self.mouse[1] <= self.padding+25:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.game.draw_text(display, "2", (0,200,0), self.padding+self.margin, self.padding, "head")
        else:
            pygame.mouse.set_cursor()
            self.game.draw_text(display, "2", (0,0,0), self.padding+self.margin, self.padding, "head")