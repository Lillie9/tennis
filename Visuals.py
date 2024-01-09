import pygame as pg
import random

screen_w = 900
screen_h = 720

screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("Tennis")

player_run = []
for i in range(2):
    img = pg.image.load(f"Player run{i}")
    player_run.append(img)

clock = pg.time.Clock()
running = True

class Ball:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0.1
        self.vy = 80

    def draw(b):
        pg.draw.circle(screen, (230,230,0), (b.x,b.y), b.r)

    def move(b):
        b.x += b.vx/100
        b.y += b.vy/100

class Bro:
    def __init__(self,x,y,w,h,opponent):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.opponent = opponent
    
    def draw(b):
        rect = (b.x, b.y, b.w, b.h)
        pg.draw.rect(screen, (0,0,0), rect)

    def move(self, ball):
        if opponent and ball.vy < 0:
            self.x += (ball.x - self.x)/100
        if not opponent and ball.vy > 0:
            self.x += (ball.x - self.x)/100


ball = Ball(screen_w/2,screen_h/2,15)
opponent = Bro(screen_w/2,260,25,50,True)
player = Bro(screen_w/2,550,50,100,False)

background = pg.transform.scale(pg.image.load("Tennisbane.png"),(screen_w,screen_h))

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type  == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            print("mouse:", mouse_x, mouse_y)

    screen.blit(background,(0,0))

    ball.draw()
    opponent.draw()
    player.draw()

    clock.tick(60)
    pg.display.flip()

pg.quit()