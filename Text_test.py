import pygame as pg

pg.font.init()

screen = pg.display.set_mode((400,400))

font = pg.font.SysFont("bahnschrift", 100)


clock = pg.time.Clock()
running = True

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type  == pg.KEYDOWN:
            if event.KEY == pg.K_ESCAPE:
                running = False

    screen.fill((255,255,255))

    text = font.render("Callibrating", True, (0,0,0))
    screen.blit(text, (100,100))

    pg.display.flip()
pg.quit()