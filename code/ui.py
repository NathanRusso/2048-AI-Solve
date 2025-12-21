import pygame as pg
from model import Model2048, Direction

class UI2048:
    """
    This holds the functions generate and manipulate the GIU the game 2048.
    """
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    COLOR_BACKGROUND = "#faf8f0"
    COLOR_BACK = "#998876"
    RUN = True

    def __init__(self, model):
        pg.init() # Starts pygame
        self.model = model
        self.screen = None
        self.player = None

    def run(self):
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("2048 Game with AI Solving!")
        self.player = pg.Rect((300, 250, 50, 50))

        while self.RUN:

            self.screen.fill(self.COLOR_BACKGROUND) # Fills (Resets) the screen to not leave trails

            pg.draw.rect(self.screen, "#ea6438", self.player)

            self.handleMovementInput()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.RUN = False

            pg.display.update() # Updates the screen to show changes

        pg.quit() # Ends pygame

    def handleMovementInput(self):
        """
        This calls the model to shift the tiles and add a new tile on the board.
        """
        key = pg.key.get_pressed()
        if key[pg.K_w] or key[pg.K_UP]:
            self.player.move_ip(0, -1)
            #self.model.playAction(Direction.UP.value)
        elif key[pg.K_s] or key[pg.K_DOWN]:
            self.player.move_ip(0, 1)
            #self.model.playAction(Direction.DOWN.value)
        elif key[pg.K_a] or key[pg.K_LEFT]:
            self.player.move_ip(-1, 0)
            #self.model.playAction(Direction.LEFT.value)
        elif key[pg.K_d] or key[pg.K_RIGHT]:
            self.player.move_ip(1, 0)
            #self.model.playAction(Direction.RIGHT.value)
    
    def getTileColor(tile: int) -> str:
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

def main():
    model = Model2048()
    game = UI2048(model)
    game.run()

if __name__ == '__main__':
    main()
