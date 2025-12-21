import pygame as pg
from model import Model2048, Direction

class UI2048:
    """
    Docstring for UI2048
    """
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    RUN = True

    def __init__(self, model):
        pg.init() # Starts pygame
        self.model = model
        self.screen = None
        self.player = None

    def run(self):
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) 
        self.player = pg.Rect((300, 250, 50, 50))

        while self.RUN:

            self.screen.fill((0, 0, 0)) # Fills (Resets) the screen to not leave trails

            pg.draw.rect(self.screen, (255, 0, 0), self.player)

            self.handleMovementInput()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.RUN = False

            pg.display.update() # Updates the screen to show changes

        pg.quit() # Ends pygame

    def handleMovementInput(self):
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

def main():
    model = Model2048()
    game = UI2048(model)
    game.run()

if __name__ == '__main__':
    main()
