import pygame
from states.state import State
from states.rush_hour import RushHour

class Level(State):
    def __init__(self, game):
        pygame.init()
        self.mouse = pygame.mouse.get_pos()        
        State.__init__(self, game)
        self.padding=100
        self.marginH=150 # margin horizontal
        self.marginV=80 # margin vertical

    def get_events(self):
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2-25 <= self.mouse[0] <= width/2+25 and height-75 <= self.mouse[1] <= height-25:
                    self.game.back()
                for i in range(self.game.numlevel):
                    row = i//5
                    col = i%5
                    if self.padding-25+col*self.marginH <= self.mouse[0] <= self.padding+25+col*self.marginH and \
                        self.padding-25+row*self.marginV <= self.mouse[1] <= self.padding+25+row*self.marginV:
                        new_state = RushHour(self.game,i+1)
                        new_state.enter_state()

    def render(self, display):
        # display.fill((255,0,255))
        display.blit(self.game.bg,[0,0])
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        pressed = False     # flag yang menunjukkan apakah terdapat tombol yang ditunjuk

        for i in range(self.game.numlevel):
            row = i//5
            col = i%5
            color=(0,0,0)
            if self.padding-25+col*self.marginH <= self.mouse[0] <= self.padding+25+col*self.marginH and \
                self.padding-25+row*self.marginV <= self.mouse[1] <= self.padding+25+row*self.marginV:
                color = (0,200,0)
                pressed=True
            self.game.draw_text(display, str(i+1), color, self.padding+col*self.marginH, self.padding+row*self.marginV, "head")

        # membuat tombol back
        if width/2-25 <= self.mouse[0] <= width/2+25 and height-75 <= self.mouse[1] <= height-25:
            pressed=True
            self.game.draw_text(display, "back", (0,200,0), width/2, height-50, "subhead")
        else:
            self.game.draw_text(display, "back", (0,0,0), width/2, height-50, "subhead")

        if(pressed):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor()
            
