import pygame as pg
import random as r
from model import Model2048, Direction

class UI2048:
    """
    This holds the functions generate and manipulate the GIU the game 2048.
    """
    MAX_BOARD_DIMENSION = 4
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 650
    COLOR_BACKGROUND = "#faf8f0"
    COLOR_BOARD = "#998876"
    RUN = True

    def __init__(self, model):
        pg.init() # Starts pygame
        pg.font.init()
        self.model = model
        self.screen = None
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
        self.tile_font = pg.font.SysFont("Clear Sans Bold", 64)
        self.mode = 0

    def run(self):
        """
        This runs, displays, and manipulates the 2048 game.
        """
        pg.display.set_caption("2048 Game with AI Solving!")
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        while self.RUN:
            self.displayCurrentGame()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.RUN = False
                self.handleMovementInput()

            if self.mode != 0:
                self.handleMovementInput()
            
            pg.display.update() # Updates the screen to show changes

        pg.quit() # Ends pygame

    def displayCurrentGame(self):
        """
        This draws the current game state.
        """
        self.screen.fill(self.COLOR_BACKGROUND) # Fills (Resets) the screen to not leave trails
        pg.draw.rect(self.screen, self.COLOR_BOARD, self.board)

        for row in range(self.MAX_BOARD_DIMENSION):
            for col in range(self.MAX_BOARD_DIMENSION):
                tile = self.model.getBoard()[row][col]
                rect_index = row * self.MAX_BOARD_DIMENSION + col
                rect = self.tiles[rect_index]
                pg.draw.rect(self.screen, self.getTileColor(tile), rect)
                if tile > 0:
                    tile_text = self.tile_font.render(str(tile), True, "#FFFFFF" if tile >= 8 else "#736452")
                    tile_text_rect = tile_text.get_rect(center=rect.center)
                    self.screen.blit(tile_text, tile_text_rect)
    
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
        if key[pg.K_r]:
            self.model.restart()
            return

        if self.mode == 0:
            if key[pg.K_w] or key[pg.K_UP]:
                self.model.playAction(Direction.UP.value)
            elif key[pg.K_s] or key[pg.K_DOWN]:
                self.model.playAction(Direction.DOWN.value)
            elif key[pg.K_a] or key[pg.K_LEFT]:
                self.model.playAction(Direction.LEFT.value)
            elif key[pg.K_d] or key[pg.K_RIGHT]:
                self.model.playAction(Direction.RIGHT.value)
            elif key[pg.K_1]:
                #self.mode = 1
                return
        elif self.mode == 1:
            if key[pg.K_0]:
                self.mode = 1
                return
            self.model.playAction(r.randint(1, 4))

def main():
    model = Model2048()
    game = UI2048(model)
    game.run()

if __name__ == '__main__':
    main()
