import os, time, pygame
# Load our scenes
from states.title import Title

class Game():
        def __init__(self):
            pygame.init()
            self.GAME_W,self.GAME_H = 960, 540
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            self.running, self.playing = True, True
            self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
            self.dt, self.prev_time = 0, 0
            self.state_stack = []
            self.load_assets()
            self.load_states()

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.update()
                self.render()

        def stop(self):
            self.playing = False
            self.running = False

        def back(self):
            self.state_stack.pop()

        def update(self):
            self.state_stack[-1].get_events()

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pygame.display.flip()

        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def draw_text(self, surface, text, color, x, y, type):
            text_surface = self.font[type].render(text, True, color)
            # text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("assets")
            self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            self.font_dir = dict()
            self.font = dict()
            self.font_dir["head"] = os.path.join(self.assets_dir, "font")
            self.font["head"]= pygame.font.Font(os.path.join(self.font_dir["head"], "RobotoMono-VariableFont_wght.ttf"), 50)
            self.font_dir["text"] = os.path.join(self.assets_dir, "font")
            self.font["text"]= pygame.font.Font(os.path.join(self.font_dir["text"], "PressStart2P-vaV7.ttf"), 10)

        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False