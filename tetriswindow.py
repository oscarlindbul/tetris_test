import pygame
from pygame.math import Vector2 as Vector
from tetrisgame import Tetris
from tetrisgame import TetroType

class TetrisWindow:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.display = pygame.display.set_mode((400, 500))
        self.display.fill((0,0,0))
        self.game_on = False

        self.field_pos = Vector(50, 50)
        self.field = TetrisField(self.field_pos, self.game)
        self.score_field = ScoreField()

    def start_loop(self):
        self.game_on = True
        while self.game_on:
            self.game.update()
            self.field.update()
            self.score_field.update()

            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_on = False
        pygame.quit()

    def draw(self):
        self.field.draw()
        self.display.blit(self.field.image, (50,50))
        pygame.display.flip()

class TetrisField:
    def __init__(self, pos, tetris_game):
        self.field_box_sep = 10
        self.gridcell_size = Vector(20, 20)
        self.field_size = Vector(self.gridcell_size.x*tetris_game.width, self.gridcell_size.y*tetris_game.height)
        self.field_pos = Vector(0, 0)
        self.next_box_size = Vector(self.gridcell_size.x*tetris_game.next_grid_width, self.gridcell_size.y*tetris_game.next_grid_height)
        self.next_box_pos = self.field_pos + Vector(self.field_size.x + self.field_box_sep, 0)
        self.tetris = tetris_game
        self.score_text_pos = self.next_box_pos + self.next_box_size/2 + Vector(0, self.next_box_size.y/2 + 30)
        self.score_text_font = pygame.font.Font("freesansbold.ttf", 18)

        self.image = pygame.Surface((self.field_size.x+self.next_box_size.x + 50, self.field_size.y + self.next_box_size.y +50))
        self.field_image = pygame.Surface((self.field_size.x + 5, self.field_size.y + 5))
        self.next_box_image = pygame.Surface((self.next_box_size.x + 5, self.next_box_size.y + 5))
        total_size = Vector(self.field_size.x + self.field_box_sep + self.next_box_size.x,
                            self.field_size.y)
        self.rect = (pos.x, pos.y, total_size.x, total_size.y)

        self.field_grid = [[None for i in range(self.tetris.width)] for j in range(self.tetris.height)]
        self.next_field_grid = [[None for i in range(self.tetris.next_grid_width)] for j in range(self.tetris.next_grid_height)]
        self.grid_group = pygame.sprite.Group()
        self.next_grid_group = pygame.sprite.Group()

    def draw(self):
        self.field_image.fill((0,0,0))
        pygame.draw.lines(self.field_image, (255,255,255),True,\
                          [self.field_pos,\
                           self.field_pos + Vector(self.field_size.x, 0),\
                           self.field_pos + self.field_size,\
                           self.field_pos + Vector(0, self.field_size.y)])
        self.grid_group.draw(self.field_image)


        pygame.draw.lines(self.next_box_image, (255,255,255), True,\
                          [Vector(0,0),\
                           Vector(self.next_box_size.x, 0),\
                           self.next_box_size,\
                           Vector(0, self.next_box_size.y)])
        self.next_grid_group.draw(self.next_box_image)

        self.image.blit(self.field_image, self.field_pos)
        self.image.blit(self.next_box_image, self.next_box_pos)

        text = self.score_text_font.render(self.score_text, True, (255,255,255), (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = self.score_text_pos
        self.image.blit(text, text_rect)


    def update(self):
        game_grid = self.tetris.get_grid()
        next_grid = self.tetris.get_next_grid()
        field_configs = ((game_grid, self.field_grid, self.tetris.width, self.tetris.height, self.grid_group),\
                         (next_grid, self.next_field_grid, self.tetris.next_grid_width, self.tetris.next_grid_height, self.next_grid_group))

        for grid, field, width, height, group in field_configs:
            for y in range(height):
                for x in range(width):
                    if grid[y][x] is None:
                        if field[y][x] is not None:
                            group.remove(field[y][x])
                        field[y][x] = None
                    elif field[y][x] is None or field[y][x] is not None and field[y][x].type != grid[y][x]:
                        if field[y][x] is not None:
                            group.remove(field[y][x])
                        cell_type = grid[y][x]
                        pos = Vector(self.gridcell_size.x * x+1, self.gridcell_size.y * y+1)
                        field[y][x] = BlockSprite(pos, self.gridcell_size, cell_type)
                        group.add(field[y][x])

        self.score_text = "Score: " + str(self.tetris.score)

        self.draw()


class ScoreField:
    def __init__(self):
        pass

    def update(self):
        pass

class BlockSprite(pygame.sprite.Sprite):

    color_maps = {
        TetroType.I: {"normal": (0, 255, 255), "light": (153, 255, 255), "dark": (0, 51, 51), "side": (0, 204, 204)},
        TetroType.O: {"normal": (255, 255, 0), "light": (255, 255, 153), "dark": (102, 102, 0), "side": (230, 230, 0)},
        TetroType.T: {"normal": (153, 51, 255), "light": (204, 153, 255), "dark": (51, 0, 102), "side": (127, 0, 255)},
        TetroType.S: {"normal": (0, 255, 0), "light": (153, 255, 153), "dark": (0, 102, 0), "side": (0, 204, 0)},
        TetroType.Z: {"normal": (255, 0, 0), "light": (255, 102, 102), "dark": (102, 0, 0), "side": (204, 0, 0)},
        TetroType.J: {"normal": (0, 0, 255), "light": (153, 153, 255), "dark": (0, 0, 102), "side": (0, 0, 204)},
        TetroType.L: {"normal": (255, 128, 0), "light": (255, 204, 153), "dark": (102, 51, 0), "side": (204, 102, 0)}
        }
    top_bottom_ratio = 0.13

    def __init__(self, pos, size, color_type):
        self.image = pygame.Surface(size)
        self.type = color_type
        self.rect = (pos[0], pos[1], size[0], size[1])
        self.draw()
        super().__init__()

    def draw(self):
        colors = BlockSprite.color_maps[self.type]
        offset = Vector(self.rect[2], self.rect[3])*BlockSprite.top_bottom_ratio
        size = Vector(self.rect[2], self.rect[3])
        in_upleft = offset
        in_upright = Vector(size.x - offset.x, offset.y)
        in_downleft = Vector(offset.x, size.y - offset.y)
        in_downright = Vector(size.x - offset.x, size.y - offset.y)
        up_left = Vector(0, 0)
        up_right = Vector(size.x, 0)
        down_left = Vector(0, size.y)
        down_right = Vector(size.x, size.y)
        self.image.fill(colors["normal"])
        pygame.draw.polygon(self.image, colors["light"],
                         [up_left,
                          in_upleft,
                          in_upright,
                          up_right,
                          up_left]
                         )
        pygame.draw.polygon(self.image, colors["dark"],
                            [down_left,
                             in_downleft,
                             in_downright,
                             down_right,
                             down_left]
                            )
        pygame.draw.polygon(self.image, colors["side"],
                            [down_left,
                             up_left,
                             in_upleft,
                             in_downleft,
                             down_left]
                            )
        pygame.draw.polygon(self.image, colors["side"],
                            [down_right,
                             up_right,
                             in_upright,
                             in_downright,
                             down_right]
                            )
        pygame.draw.line(self.image, (0, 0, 0), up_left, in_upleft)
        pygame.draw.line(self.image, (0, 0, 0), down_left, in_downleft)
        pygame.draw.line(self.image, (0, 0, 0), up_right, in_upright)
        pygame.draw.line(self.image, (0, 0, 0), down_right, in_downright)

