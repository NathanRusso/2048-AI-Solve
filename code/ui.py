from enum import Enum
import random as r
import pygame as pg
from model import Model2048, Direction
from expectiminimax import Expectiminimax2048
from montecarlo import MonteCarlo2048


class UIMode(Enum):
    """
    A class that holds the different game modes.
    """
    MANUAL = 0
    RANDOM = 1
    EXPECTIMINIMAX = 2
    MCTS = 3


class UI2048:
    """
    This holds the functions generate and manipulate the GIU the game 2048.
    """
    MAX_BOARD_DIMENSION = 4
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 650
    COLOR_SCREEN = "#faf8f0"
    COLOR_BOARD = "#998876"
    COLOR_LABEL_TEXT = "#736452"
    COLOR_BUTTON_TEXT = "#FFFFFF" # "#f2f0e5"
    COLOR_BUTTON_BACKGROUND = COLOR_BOARD
    RUN = True

    def __init__(self, model, expectiminimax, mcts):
        """
        This sets up the variables need for the UI to function.
        
        :param model: A game model for 2048.
        :param expectiminimax: A Expectiminimax solver to chose the next direction.
        :param mcts: A Monte Carlo Tree Search solver to chose the next direction.
        """
        pg.init() # Starts pygame
        pg.font.init()
        self.model = model
        self.expectiminimax = expectiminimax
        self.mcts = mcts
        self.screen = None
        self.clock = pg.time.Clock()
        self.board = pg.Rect((10, 110, 530, 530))
        self.tiles = [
            pg.Rect((20, 120, 120, 120)),
            pg.Rect((150, 120, 120, 120)),
            pg.Rect((280, 120, 120, 120)),
            pg.Rect((410, 120, 120, 120)),
            pg.Rect((20, 250, 120, 120)),
            pg.Rect((150, 250, 120, 120)),
            pg.Rect((280, 250, 120, 120)),
            pg.Rect((410, 250, 120, 120)),
            pg.Rect((20, 380, 120, 120)),
            pg.Rect((150, 380, 120, 120)),
            pg.Rect((280, 380, 120, 120)),
            pg.Rect((410, 380, 120, 120)),
            pg.Rect((20, 510, 120, 120)),
            pg.Rect((150, 510, 120, 120)),
            pg.Rect((280, 510, 120, 120)),
            pg.Rect((410, 510, 120, 120))
        ]
        self.buttons = [
            pg.Rect((565, 10, 200, 30)),
            pg.Rect((565, 50, 200, 30)),
            pg.Rect((565, 90, 200, 30)),
            pg.Rect((565, 130, 200, 30))
        ]
        self.tile_font = pg.font.SysFont("Clear Sans Bold", 64)
        self.info_font = pg.font.SysFont("Clear Sans Bold", 32)
        self.mode = UIMode.MANUAL.value

    def run(self):
        """
        This runs, displays, and manipulates the 2048 game.
        """
        pg.display.set_caption("2048 Game with AI Solving!")
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        while self.RUN:
            self.displayCurrentGame()

            mouse = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT: self.RUN = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = mouse
                    for index, button in enumerate(self.buttons):
                        button_min_x, button_min_y = button.topleft
                        button_max_x, button_max_y = button.bottomright
                        if (button_min_x <= mouse_x <= button_max_x) and (button_min_y <= mouse_y <= button_max_y):
                            self.setMode(index)

                if self.mode == UIMode.MANUAL.value: self.handleMovementInput() # Handle per event if manual

            if self.mode != UIMode.MANUAL.value: self.handleMovementInput()
            
            pg.display.update() # Updates the screen to show changes
            if self.mode != UIMode.MANUAL.value:
                self.clock.tick(10) # Update runs at 10 frames/second
            
        pg.quit() # Ends pygame

    def displayCurrentGame(self):
        """
        This draws the current game state.
        """
        self.screen.fill(self.COLOR_SCREEN) # Fills (Resets) the screen to not leave trails
        pg.draw.rect(self.screen, self.COLOR_BOARD, self.board)

        self.drawLabel(f"Best Score: {self.model.getBestScore()}", (10, 10))
        self.drawLabel(f"Current Score: {self.model.getScore()}", (10, 40))
        if self.model.gameOver(): self.drawLabel("GAME OVER!", (10, 70))

        self.drawButton(UIMode.MANUAL.value, "Manual Play!")
        self.drawButton(UIMode.RANDOM.value, "Random Play!")
        self.drawButton(UIMode.EXPECTIMINIMAX.value, "Expectiminimax!")
        self.drawButton(UIMode.MCTS.value, "Monte Carlo!")

        current_board = self.model.getBoard()
        for row in range(self.MAX_BOARD_DIMENSION):
            for col in range(self.MAX_BOARD_DIMENSION):
                tile = current_board[row][col]
                rect_index = row * self.MAX_BOARD_DIMENSION + col
                rect = self.tiles[rect_index]
                pg.draw.rect(self.screen, self.getTileColor(tile), rect)
                if tile > 0:
                    tile_text = self.tile_font.render(str(tile), True, "#FFFFFF" if tile >= 8 else "#736452")
                    tile_text_rect = tile_text.get_rect(center=rect.center)
                    self.screen.blit(tile_text, tile_text_rect)

    def drawLabel(self, label_display_text: str, label_top_left: tuple):
        """
        This draws a label on the screen.
        
        :param label_display_text: The text the label will show.
        :type label_display_text: str
        :param label_top_left: The top left location on the text rectangle.
        :type label_top_left: tuple
        """
        text = self.info_font.render(label_display_text, True, self.COLOR_LABEL_TEXT)
        text_rect = text.get_rect(topleft=label_top_left)
        self.screen.blit(text, text_rect)        

    def drawButton(self, button_rect_index: int, button_display_text: str):
        """
        This draws a buttons on the screen.
        
        :param button_rect_index: The index in the buttons list that holds the rectangle position
        :type button_rect: int
        :param button_text: The text the button will show
        :type button_text: str
        """
        rect = self.buttons[button_rect_index]
        pg.draw.rect(self.screen, self.COLOR_BUTTON_BACKGROUND, rect)
        button_text = self.info_font.render(button_display_text, True, self.COLOR_BUTTON_TEXT)
        button_text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, button_text_rect)

    def getTileColor(self, tile: int) -> str:
        """
        This gets the color of the given tile.
        
        :param tile: The given tile value.
        :type tile: int
        :return: The hex color of the tile.
        :rtype: str
        """
        match tile:
            case 0: return "#bbac97"
            case 2: return "#ede4da"
            case 4: return "#e8d8b5"
            case 8: return "#ebb278"
            case 16: return "#ec9761"
            case 32: return "#eb805e"
            case 64: return "#ea6438"
            case 128: return "#e9cf70"
            case 256: return "#edd25e"
            case 512: return "#e8c84c"
            case 1024: return "#e7c53a"
            case 2048: return "#e7c226"
            case 4096: return "#66d56c"
            case 8192: return "#24C8B5"
            case 16384: return "#1D72C1"
            case 32768: return "#7050d2"
            case _: return "#000000"

    def handleMovementInput(self):
        """
        This calls the model to shift the tiles and add a new tile on the board.
        """
        key = pg.key.get_pressed()

        if key[pg.K_r]: # Reset
            self.setMode(UIMode.MANUAL.value)
            return
        
        match self.mode:
            case UIMode.MANUAL.value:
                if key[pg.K_1]:
                    self.setMode(UIMode.RANDOM.value)
                elif key[pg.K_2]:
                    self.setMode(UIMode.EXPECTIMINIMAX.value)
                elif key[pg.K_3]:
                    self.setMode(UIMode.MCTS.value)
                elif key[pg.K_w] or key[pg.K_UP]:
                    self.model.playAction(Direction.UP.value)
                elif key[pg.K_s] or key[pg.K_DOWN]:
                    self.model.playAction(Direction.DOWN.value)
                elif key[pg.K_a] or key[pg.K_LEFT]:
                    self.model.playAction(Direction.LEFT.value)
                elif key[pg.K_d] or key[pg.K_RIGHT]:
                    self.model.playAction(Direction.RIGHT.value)
            case UIMode.RANDOM.value:
                if key[pg.K_0]:
                    self.setMode(UIMode.MANUAL.value)
                elif key[pg.K_2]:
                    self.setMode(UIMode.EXPECTIMINIMAX.value)
                elif key[pg.K_3]:
                    self.setMode(UIMode.MCTS.value)
                else:
                    self.model.playAction(r.randint(1, 4))
            case UIMode.EXPECTIMINIMAX.value:
                if key[pg.K_0]:
                    self.setMode(UIMode.MANUAL.value)
                elif key[pg.K_1]:
                    self.setMode(UIMode.RANDOM.value)
                elif key[pg.K_3]:
                    self.setMode(UIMode.MCTS.value)
                else:
                    self.model.playAction(self.expectiminimax.getNextDirection(self.model.getBoard()))
            case UIMode.MCTS.value:
                if key[pg.K_0]:
                    self.setMode(UIMode.MANUAL.value)
                elif key[pg.K_1]:
                    self.setMode(UIMode.RANDOM.value)
                elif key[pg.K_2]:
                    self.setMode(UIMode.EXPECTIMINIMAX.value)
                else:
                    self.model.playAction(self.mcts.getNextDirection(self.model.getBoard()))
    
    def setMode(self, mode: int):
        """
        This resets the board and switches modes.
        
        :param mode: The ints value for the mode.
        :type mode: int
        """
        self.model.restart()
        self.mode = mode

def main():
    model = Model2048()
    expectiminimax = Expectiminimax2048(5, 2) # Search depth of 5 is the max before the time increase becomes too much!
    montecarlo = MonteCarlo2048(1000, 200)
    game = UI2048(model, expectiminimax, montecarlo)
    game.run()

if __name__ == '__main__':
    main()
