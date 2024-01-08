import pygame as pg
import Reciever 
import random

screen_w = 900
screen_h = 720

min_power = 120
win_speed = -100

screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("Tennis")

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
opponent = Bro(screen_w/2,100,25,50,True)
player = Bro(screen_w/2,400,50,100,False)

background = pg.transform.scale(pg.image.load("Tennisbane.png"),(screen_w,screen_h))

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type  == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    screen.blit(background,(0,0))

    #Movement
    data = Reciever.read()
    if data != None:
        x,y,z = data
        snit = (x + y + z)/3
        if snit > min_power:
            print("slay")
            if (player.y - ball.y) < 25 and (player.y - ball.y) > -50:
                if ball.vy > 0:
                    ball.vy *= -snit/100
                    ball.vx *= random.random() * 2 - 1
    
    if (ball.y - opponent.y) < 10 and ball.vy > win_speed:
        ball.vy *= -1
        ball.vx *= (random.random() * 2 - 1) * 25


    ball.draw()
    ball.move()
    opponent.draw()
    opponent.move(ball)
    player.draw()
    player.move(ball)

    clock.tick(60)
    pg.display.flip()

pg.quit()