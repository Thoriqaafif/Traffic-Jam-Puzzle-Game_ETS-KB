# berisi kelas game dan kelas generate
# kelas game mengatur semua yang dibutuhkan game
# kelas generate melakukan generate game secara random
import os, time, pygame
import random
# Load our scenes
from states.title import Title
from tkinter import messagebox

class Game():
        def __init__(self):
            pygame.init()   # inisialisasi pygame

            # mengatur canvas dan screen game
            # keduanya memiliki lebar 800 dan tinggi 600
            self.GAME_W,self.GAME_H = 800, 600
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 800, 600
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))

            # mengatur icon and caption
            pygame.display.set_caption("Traffic Jam Puzzle")
            icon=pygame.image.load("assets/img/icon.png")
            pygame.display.set_icon(icon)

            self.running, self.playing = True, True     # status game, true berarti masih berjalan
            self.state_stack = []                       # menyimpan game state
            self.numlevel=0                             # level yang telah dibuat saat ini
            self.load_assets()                          # load gambar, font, dan text yang dibutuhkan
            self.load_states()                          # load states awal

        # method untuk keluar dari game
        def stop(self):
            # jika pemain menekan yes
            # status game diubah ke false
            # game berhenti
            stop=messagebox.askyesno('Quit','Do you want to quit?')
            if stop:
                self.playing = False
                self.running = False

        # method untuk kembali ke 
        # game state sebelumnya
        def back(self):
            self.state_stack.pop()

        # method untuk mendapat update event
        # pada game state saat ini
        def update(self):
            self.state_stack[-1].get_events()

        # method untuk merender aset yang dimiliki
        # game state saat ini
        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pygame.display.flip()

        # meletakkan text pada layar
        def draw_text(self, surface, text, color, x, y, type):
            # memberi border pada text bertipe head dan subhead
            if(type=="head" or type=="subhead"):
                global text_surface
                global text_rect
                text_surface = self.font[type].render(text, True, (250,250,250))
                text_rect = text_surface.get_rect()
                text_rect.center = (x+2,y+2)
                surface.blit(text_surface, text_rect)
                text_rect.center = (x+2,y-2)
                surface.blit(text_surface, text_rect)
                text_rect.center = (x-2,y+2)
                surface.blit(text_surface, text_rect)
                text_rect.center = (x-2,y-2)
                surface.blit(text_surface, text_rect)
            
            text_surface = self.font[type].render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        # method untuk mengambil assets pada folder assets
        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("assets")

            # load font
            self.font_dir = dict()
            self.font = dict()
            self.font_dir["head"] = os.path.join(self.assets_dir, "font")
            self.font["head"]= pygame.font.Font(os.path.join(self.font_dir["head"], "PressStart2P-vaV7.ttf"), 40)
            self.font_dir["subhead"] = os.path.join(self.assets_dir, "font")
            self.font["subhead"]= pygame.font.Font(os.path.join(self.font_dir["subhead"], "PressStart2P-vaV7.ttf"), 30)
            self.font_dir["text"] = os.path.join(self.assets_dir, "font")
            self.font["text"]= pygame.font.Font(os.path.join(self.font_dir["text"], "PressStart2P-vaV7.ttf"), 10)
            self.bg = pygame.image.load("./assets/img/batik1.png")
            
            # tanah tempat becak dan mobil
            self.tanah = pygame.image.load("./assets/img/tanah.png")
            self.tanah = pygame.transform.scale(self.tanah,(70,70))

            # becak
            self.becak = pygame.image.load("./assets/img/delman.png")
            self.becak = pygame.transform.scale(self.becak,(105,70))
            self.becaklogo = pygame.transform.scale(self.becak,(150,100))

            # mobil ukuran 3
            self.car1 = pygame.image.load("./assets/img/car1.png")
            self.car1H = pygame.transform.scale(self.car1,(200,70))
            self.car1V = pygame.transform.rotate(self.car1H, 90)

            # mobil ukuran 2
            self.car2 = pygame.image.load("./assets/img/car2.png")
            self.car2H = pygame.transform.scale(self.car2,(140,70))
            self.car2V = pygame.transform.rotate(self.car2H, 90)

        # awal game masuk ke state title
        # buat state title, masukkan state ke stack
        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)
            
        # method untuk membuat level baru
        # menambah variabel numlevel
        # generate level dengan memanggil kelas Generate
        def newLevel(self):
            self.numlevel += 1
            Generate(self.numlevel)

        # method untuk mencari hint
        # panggil method search di kelas generate
        # return board ke-2, yaitu langkah selanjutnya
        def hint(self,board):
            path = Generate.search(board)
            # return path[1]
            if(path != [board]):
                return path[1]
            else:
                return None

N = 6
EMPTY_SPACE = '_'
MAIN_OBJECT = 'A'
START_ROW = 2       # row of the main object

class Generate():

    def __init__(self, level):
        # mendapat papan permainan secara random
        # mendapat langkah penyelesaian
        # ulangi hingga panjang langkah penyelesaian
        # lebih dari sama dengan 15
        self.get_board()
        self.path=Generate.search(self.board)
        while len(self.path) < 15:
            self.get_board()
            self.path=Generate.search(self.board)

        # membuat file txt berisi level dan hint
        self.make_level_txt(level)
        self.make_hint_txt(level)

    def get_board(self):
        # Huruf besar melambangkan horizontal
        # Huruf kecil melambangkan vertical.
        self.board = [[EMPTY_SPACE] * 6 for _ in range(N)]
        # Inisialisasi objek utama berada pada
        # baris 2 dan kolom acak
        start_col = random.randrange(N - 2)
        self.board[START_ROW][start_col] = self.board[START_ROW][start_col + 1] = MAIN_OBJECT

        # tambah objek secara random
        num_attempts = 0
        for i in range(random.randrange(6, 10)):    # buat 6 hingga 9 objek
            car_len = random.randrange(2, 4)        # objek berukuran 2 atau 3 kotak
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
                # jika kosong, mobil bermasalah sehingga harus dibuang dan membuat ulang
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

                # agar tidak terlalu lama, berhenti ketika
                # telah melakukan 1000 iterasi
                if num_attempts > 1000:
                    break

    def board_str(board):
        return '\n'.join(' '.join(_) for _ in board)

    def copy_board(board):
        return [_[:] for _ in board]

    def is_solved(board):
        # cek apakah terdapat objek yang menghalangi objek utama
        # dengan cek apakah kotak pada baris ke-2 kosong atau tidak
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
    # menggerakkan objek yang dapat digerakkan
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

    # method untuk mencari penyelesaian menggunakan BFS
    def search(board):
        queue = [[board]]  # queue untuk menyimpan path
                           # current state pada path[-1]
        board_hash_set = set()  # menyimpan sate yang visited

        while queue:
            # keluarkan nilai pada queue
            path = queue.pop(0)

            # jika telah selesai, return path
            if Generate.is_solved(path[-1]):
                return path

            # kunjungi semua kemungkinan state
            # jika state tidak ada pada board_hash_set
            # masukkan pada queue
            for next_state in Generate.get_next_states(path[-1]):
                if Generate.board_str(next_state) not in board_hash_set:
                    board_hash_set.add(Generate.board_str(next_state))
                    queue.append((path + [next_state]))

        # jika tidak ada penyelesaiannya
        # return array kosong
        return []

    # meletakkan board yang telah dibuat ke file txt
    def make_level_txt(self, level):  # print board to txt file
        letter = ['A', '_']
        blocks = []

        # untuk objek utama, beri karakter 'A'
        # dengan orientasi horizontal 'h',
        # panjang 2, baris 2, dan kolom i
        # kolom dicek dengan melakukan iterasi
        for i in range(6):
            if self.board[2][i] == 'A':
                blocks.append(['h', 2, 2, i])
                break

        # memasukkan objek lain dengan mengecek setiap kotak
        for i in range(6):
            length = 0
            for j in range(6):
                # proses jika objek pada kotak belum dimasukkan ke file
                if self.board[i][j] not in letter:
                    # objek horizontal
                    if self.board[i][j].isupper():
                        if self.board[i][j] == self.board[i][j + 1]:
                            # cek panjang
                            if j + 2 < 6 and self.board[i][j] == self.board[i][j + 2]:
                                length = 3
                            else:
                                length = 2
                            # masukkan nilai objek ke file
                            letter.append(self.board[i][j])
                            blocks.append(['h', length, i, j])

                    # objek vertikal
                    else:
                        if self.board[i][j] == self.board[i + 1][j]:
                            # cek panjang
                            if i + 2 < 6 and self.board[i][j] == self.board[i + 2][j]:
                                length = 3
                            else:
                                length = 2
                            # masukkan nilai objek ke file
                            letter.append(self.board[i][j])
                            blocks.append(['v', length, i, j])

        # buat file dengan nama "/assets/level/game(level).txt"
        strout = "./assets/level/game"+str(level)+".txt"
        out = open(strout, 'w')
        for i in blocks:
            out.write('{}, {}, {}, {}\n'.format(i[0], i[1], i[2], i[3]))

    # membuat hint dan memasukkan ke file txt
    def make_hint_txt(self, level):
        file_path = "./assets/hint/game{}.txt".format(level)
        
        with open(file_path, 'w') as file:
            for board in self.path:
                for row in board:
                    row_str = ' '.join(['_' if cell == 0 else str(cell) for cell in row])
                    file.write(row_str + '\n')
                file.write('\n')  # Add an empty line between matrices    