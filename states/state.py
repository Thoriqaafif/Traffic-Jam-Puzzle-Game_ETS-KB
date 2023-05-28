# abstract class untuk state

class State():
    # inisialisasi dengan atribut game dan state sebelumnya
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    # abstract method untuk render
    def render(self, surface):
        pass
    # abstract method untuk mendapat event
    def get_events(self):
        pass

    # method untuk memasuki state
    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    # method untuk keluar dari state
    def exit_state(self):
        self.game.state_stack.pop()