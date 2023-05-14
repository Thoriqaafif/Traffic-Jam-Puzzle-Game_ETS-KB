import pygame
from states.state import State

class Help(State):
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
                # back
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+175 <= self.mouse[1] <= height/2+225:
                    self.game.back()

    def render(self, display):
        display.fill((255,0,255))
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()

        self.game.draw_text(display, "Help", (0,0,0), width/2, height/2-200, "head")
        i=0
        file = open('./assets/text/help.txt', 'r')
        Lines = file.read().splitlines()
        for line in Lines:
            self.game.draw_text(display, line, (0,0,0), width/2, height/2-100+i, "text")
            i+=20

        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+175 <= self.mouse[1] <= height/2+225:
            self.game.draw_text(display, "Back", (0,200,0), width/2, height/2+200, "head")
        else:
            self.game.draw_text(display, "Back", (0,0,0), width/2, height/2+200, "head")