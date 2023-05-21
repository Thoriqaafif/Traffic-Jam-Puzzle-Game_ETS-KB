import os, time, pygame
import random
# Load our scenes
from states.title import Title
from tkinter import messagebox

class Game():
        def __init__(self):
            pygame.init()
            self.GAME_W,self.GAME_H = 800, 600
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 800, 600
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            # set icon and caption
            pygame.display.set_caption("Traffic Jam Puzzle")
            icon=pygame.image.load("assets/icon.png")
            pygame.display.set_icon(icon)
            self.running, self.playing = True, True
            # self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
            self.dt, self.prev_time = 0, 0
            self.state_stack = []
            self.level=0        #current level
            self.numlevel=0     #current number of level
            self.load_assets()
            self.load_states()
            # self.newLevel()

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.update()
                self.render()

        def stop(self):
            stop=messagebox.askyesno('Quit','Do you want to quit?')
            if stop:
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

        # meletakkan text pada layar
        def draw_text(self, surface, text, color, x, y, type):
            text_surface = self.font[type].render(text, True, color)
            # text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        # meletakkan gambar pada layar
        def draw_image():
            pass

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("assets")
            self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            self.font_dir = dict()
            self.font = dict()
            self.font_dir["head"] = os.path.join(self.assets_dir, "font")
            self.font["head"]= pygame.font.Font(os.path.join(self.font_dir["head"], "PressStart2P-vaV7.ttf"), 30)
            self.font_dir["text"] = os.path.join(self.assets_dir, "font")
            self.font["text"]= pygame.font.Font(os.path.join(self.font_dir["text"], "PressStart2P-vaV7.ttf"), 10)
            self.bg = pygame.image.load("./assets/background.jpeg")
            self.car = pygame.image.load("./assets/car.png")
            self.car = pygame.transform.scale(self.car,(140,70))

        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False
            
        def newLevel(self):
            self.numlevel += 1
            Generate(self.numlevel)

        def search(board):
            Generate.search(board)

        def tes(self,board):
            Generate.board_str(board)

N = 6
EMPTY_SPACE = '_'
MAIN_OBJECT = 'A'
START_ROW = 2       # row of the main object
PLIES = {}

class Generate():

    def __init__(self, level):
        self.get_board()
        self.path=Generate.search(self.board)
        while len(self.path) < 15:
            self.get_board()
            self.path=Generate.search(self.board)
        self.make_level_txt(level)

    def get_board(self):
        # Uppercase is horizontal, lowercase is vertical.
        self.board = [[EMPTY_SPACE] * 6 for _ in range(N)]
        # Initialize the main object in a random column.
        start_col = random.randrange(N - 2)
        self.board[START_ROW][start_col] = self.board[START_ROW][start_col + 1] = MAIN_OBJECT

        # Add more cars.
        num_attempts = 0
        for i in range(random.randrange(6, 10)):    # make 6 until 9 cars
            car_len = random.randrange(2, 4)        # car length is 2 or 3 square
            while True:
                vertical = random.randrange(2) == 0
                # if vertical car, row is in 0 until N - carlength
                # if horizontal car, row is in 0 until N
                r = random.randrange(N - (car_len - 1) * int(vertical))
                # if vertical car, col is in 0 until N
                # if horizontal car, col is in 0 until N - carlength
                c = random.randrange(N - (car_len - 1) * int(not vertical))
                is_clear = True     # cek board yang dibuat dapat dibuat atau bermasalah
                # cek apakah kotak yang akan ditempati kosong atau tidak
                # jika kosong, mobil bermasalah sehingga harus dibuat ulang
                for j in range(car_len):
                    if self.board[r + j * int(vertical)][c + j * int(not vertical)] != EMPTY_SPACE:
                        is_clear = False
                        break

                # memberi kode untuk tiap mobil, memberhentikan iterasi
                if is_clear:
                    car_char = chr(ord('b' if vertical else 'B') + i)
                    for j in range(car_len):
                        self.board[r + j * int(vertical)][c + j *
                                                    int(not vertical)] = car_char
                    break

                num_attempts += 1
                if num_attempts > 1000:
                    # We have enough cars anyway.
                    break

    def board_str(board):
        return '\n'.join(' '.join(_) for _ in board)


    def copy_board(board):
        return [_[:] for _ in board]


    def is_solved(board):
        # Find any obstacles between the ice cream truck and the right edge.
        for i in range(N - 1, -1, -1):
            char_i = board[START_ROW][i]
            if char_i == EMPTY_SPACE:
                continue
            elif char_i == MAIN_OBJECT:
                return True
            else:
                return False

        return True

    # mendapatkan langkah selanjutnya
    def get_next_states(board):
        processed_chars_set = set([EMPTY_SPACE])
        next_states = []
        for r in range(N):
            for c in range(N):
                char = board[r][c]
                if char not in processed_chars_set:
                    processed_chars_set.add(char)
                    delta_r = 0
                    delta_c = 0
                    is_vertical = not char.isupper()
                    if is_vertical:
                        delta_r = 1
                    else:
                        delta_c = 1

                    # Find the extrema
                    min_r, max_r = r, r
                    min_c, max_c = c, c
                    while min_r - delta_r >= 0 and min_c - delta_c >= 0 and board[min_r - delta_r][min_c - delta_c] == char:
                        min_r -= delta_r
                        min_c -= delta_c

                    while max_r + delta_r < N and max_c + delta_c < N and board[max_r + delta_r][max_c + delta_c] == char:
                        max_r += delta_r
                        max_c += delta_c

                    if min_r - delta_r >= 0 and min_c - delta_c >= 0 and board[min_r - delta_r][min_c - delta_c] == EMPTY_SPACE:
                        next_state = Generate.copy_board(board)
                        next_state[min_r - delta_r][min_c - delta_c] = char
                        next_state[max_r][max_c] = EMPTY_SPACE
                        next_states.append(next_state)

                    if max_r + delta_r < N and max_c + delta_c < N and board[max_r + delta_r][max_c + delta_c] == EMPTY_SPACE:
                        next_state = Generate.copy_board(board)
                        next_state[min_r][min_c] = EMPTY_SPACE
                        next_state[max_r + delta_r][max_c + delta_c] = char
                        next_states.append(next_state)

        return next_states




    def search(board):
        queue = [(0, [board])]
        board_hash_set = set()

        while queue:
            ply, path = queue.pop(0)
            if ply not in PLIES:
                PLIES[ply] = 1
            else:
                PLIES[ply] += 1

            if Generate.is_solved(path[-1]):
                return path

            for next_state in Generate.get_next_states(path[-1]):
                if Generate.board_str(next_state) not in board_hash_set:
                    board_hash_set.add(Generate.board_str(next_state))
                    queue.append((ply + 1, path + [next_state]))

        return []

    def make_level_txt(self, level):  # print board to txt file
        letter = ['A', '_']
        blocks = []
        for i in range(6):
            if self.board[2][i] == 'A':
                blocks.append(['h', 2, 2, i])
                break

        for i in range(6):
            length = 0
            for j in range(6):
                if self.board[i][j] not in letter:
                    if self.board[i][j].isupper():
                        if self.board[i][j] == self.board[i][j + 1]:
                            if j + 2 < 6 and self.board[i][j] == self.board[i][j + 2]:
                                length = 3
                            else:
                                length = 2
                            letter.append(self.board[i][j])
                            blocks.append(['h', length, i, j])

                    else:
                        if self.board[i][j] == self.board[i + 1][j]:
                            if i + 2 < 6 and self.board[i][j] == self.board[i + 2][j]:
                                length = 3
                            else:
                                length = 2
                            letter.append(self.board[i][j])
                            blocks.append(['v', length, i, j])

        strout = "./assets/level/game"+str(level)+".txt"
        out = open(strout, 'w')
        for i in blocks:
            out.write('{}, {}, {}, {}\n'.format(i[0], i[1], i[2], i[3]))
            print(i)


    def play():
        while True:
            board = Generate.get_board()
            path = Generate.search(board)
            # print('Solved length: {}'.format(len(path)))
            # print(PLIES)
            if len(path) >= 15:
                Generate.make_level_txt(path[0])
                # for i in path[0]:
                #     print(i)
                print('\n\n'.join(Generate.board_str(_) for _ in path))
                # RushHour()
                break