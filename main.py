from tetriswindow import TetrisWindow
from tetrisgame import Tetris

game_size = (10, 20)
difficulty = 1

game = Tetris(game_size, difficulty)
window = TetrisWindow(game)
window.start_loop()