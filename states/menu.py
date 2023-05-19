import pygame
from states.state import State
from states.help import Help
from states.rushhour import GenerateGame

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
                # go to help state
                if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
                    new_state = GenerateGame.play()
                    new_state.enter_state()
                elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
                    new_state = Help(self.game)
                    new_state.enter_state()
                # quit game
                elif width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
                    self.game.stop()

    def render(self, display):
        display.fill((255, 0, 255))
        width = self.game.SCREEN_WIDTH
        height = self.game.SCREEN_HEIGHT
        self.mouse = pygame.mouse.get_pos()
        self.game.draw_text(display, "Main Menu", (0, 0, 0),
                            width/2, height/2-200, "head")

        # tombol play
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2-100 <= self.mouse[1] <= height/2-50:
            self.game.draw_text(display, "Play", (0, 200, 0),
                                width/2, height/2-75, "head")
        else:
            self.game.draw_text(display, "Play", (0, 0, 0),
                                width/2, height/2-75, "head")

        # tombol help
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2 <= self.mouse[1] <= height/2+50:
            self.game.draw_text(display, "Help", (0, 200, 0),
                                width/2, height/2+25, "head")
        else:
            self.game.draw_text(display, "Help", (0, 0, 0),
                                width/2, height/2+25, "head")

        # tombol quit
        if width/2-75 <= self.mouse[0] <= width/2+75 and height/2+100 <= self.mouse[1] <= height/2+150:
            self.game.draw_text(display, "Quit", (0, 200, 0),
                                width/2, height/2+125, "head")
        else:
            self.game.draw_text(display, "Quit", (0, 0, 0),
                                width/2, height/2+125, "head")
