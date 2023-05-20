import pygame
from states.state import State
from states.rush_hour import GenerateGame

class Level(State):
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
                    GenerateGame.play()

    def render(self, display):
        display.fill((255,0,255))
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()

        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+25 <= self.mouse[1] <= height/2+75:
            self.game.draw_text(display, "1", (0,200,0), width/2, height/2+50, "head")
        else:
            self.game.draw_text(display, "1", (0,0,0), width/2, height/2+50, "head")