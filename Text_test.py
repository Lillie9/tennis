import pygame as pg

pg.font.init()

screen = pg.display.set_mode((400,400))

font = pg.font.SysFont("bahnschrift", 100)


clock = pg.time.Clock()
running = True

background = pg.transform.scale(pg.image.load("Tennisbane.png"),(400,400))

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type  == pg.KEYDOWN:
            if event.KEY == pg.K_ESCAPE:
                running = False

    screen.blit(background,(0,0))
    text = font.render("Callibrating", True, (0,0,0))
    screen.blit(text, (100,100))

    pg.display.flip()
pg.quit()