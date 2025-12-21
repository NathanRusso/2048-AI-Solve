import pygame as pg

pg.init() # Starts pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
run = True

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

player = pg.Rect((300, 250, 50, 50))

while run:

    screen.fill((0, 0, 0)) # Fills (Resets) the screen to not leave trails

    pg.draw.rect(screen, (255, 0, 0), player)

    key = pg.key.get_pressed()
    if key[pg.K_a]:
        player.move_ip(-1, 0)
    elif key[pg.K_d]:
        player.move_ip(1, 0)
    elif key[pg.K_w]:
        player.move_ip(0, -1)
    elif key[pg.K_s]:
        player.move_ip(0, 1)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update() # Updates the screen to show changes

pg.quit() # Ends pygame
