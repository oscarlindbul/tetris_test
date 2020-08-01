import pygame
from pygame.locals import K_UP, K_RIGHT, K_LEFT, K_DOWN, K_a, K_d
import enum

class Tetris:

    MOVE_EVENT = pygame.USEREVENT + 1
    RIGHTKEY = K_RIGHT
    LEFTKEY = K_LEFT
    ROTATELEFT = K_a
    ROTATERIGHT = K_d

    def __init__(self, size, difficulty):
        self.width = size[0]
        self.height = size[1]
        self.next_grid_width = 6
        self.next_grid_height = 6
        self.difficulty = difficulty
        self.next_tetro = None
        self.score = 0

        self.grid = [[None for i in range(self.width)] for j in range(self.height)]
        self.next_tetro_grid = [[None for i in range(self.next_grid_width)] for j in range(self.next_grid_height)]
        self.move_delay = 1000
        pygame.time.set_timer(Tetris.MOVE_EVENT, self.move_delay)

        ## debug code
        self.player_pos = [5, 0]
        self.grid[self.player_pos[1]][self.player_pos[0]] = TetroType.O
        self.next_tetro_grid[2][2] = TetroType.L
        self.c = 1

    def update(self):
        self.c += 1
        if pygame.event.get(Tetris.MOVE_EVENT):
            pass
            # What to do when player should move down
        for event in pygame.event.get(pygame.KEYDOWN):
            pass
            # handle key presses


    def start_game(self):
        pass

    def get_random_tetro(self):
        pass

    def set_grid(self, x, y, tetro_type):
        pass

    def set_next_grid(self, x, y, tetro_type):
        pass

    def get_grid(self):
        return self.grid

    def get_next_grid(self):
        return self.next_tetro_grid

class TetroType(enum.Enum):
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7

class Tetromino:

    tetro_builds = {
        TetroType.I: [(0, -2), (0, -1), (0,0), (0, 1)],
        TetroType.O: [(0, 0), (0, -1), (1, 0), (1, -1)],
        TetroType.T: [(-1, 0), (0, 0), (1, 0), (0, 1)],
        TetroType.S: [(-1, 1), (0, 1), (0, 0), (1, 0)],
        TetroType.Z: [(-1, -1), (0, -1), (0, 0), (1, 0)],
        TetroType.J: [(0, -1), (0, 0), (0, 1), (-1, 1)],
        TetroType.L: [(0, -1), (0, 0), (0, 1), (1, 1)]
    }

    def __init__(self, center_pos, t_type, rotation_state=0):
        self.center_pos = center_pos
        self.t_type = t_type
        self.rotation_state = rotation_state

    def move(self, vector):
        pass

    def rotate(self, increment):
        pass