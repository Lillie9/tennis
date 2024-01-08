import pygame as pg
import Reciever 
import random

screen = pg.display.set_mode((1000,600))
pg.display.set_caption("Tennis")

clock = pg.time.Clock()
running = True

class Ball:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 40

    def draw(b):
        pg.draw.circle(screen, (230,230,0), (b.x,b.y), b.r)

    def move(b):
        b.x += b.vx/100
        b.y += b.vy/100

class Bro:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(b):
        rect = (b.x, b.y, b.w, b.h)
        pg.draw.rect(screen, (0,0,0), rect)

    def move(self, ball):
        self.x = ball.x

ball = Ball(500,300,15)
opponent = Bro(100,100,25,50)
player = Bro(850,400,50,100)

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type  == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    screen.fill((255,255,255))

    #Movement
    data = Reciever.read()
    if data != None:
        x,y,z = data
        snit = (x + y + z)/3
        if snit > 120:
            print("slay")
            if (player.y - ball.y) < 25 and (player.y - ball.y) > -50:
                if ball.vy > 0:
                    ball.vy *= -snit/100
    
    if (ball.y - opponent.y) < 10 and ball.vy > -100:
        ball.vy *= -1


    ball.draw()
    ball.move()
    opponent.draw()
    opponent.move(ball)
    player.draw()
    player.move(ball)



    pg.display.flip()
pg.quit()