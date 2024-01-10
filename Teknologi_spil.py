import pygame as pg
import Reciever 
import random

screen_w = 900
screen_h = 720

tick = 0

min_power = 120
win_speed = -100

screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("Tennis")

player_run = []
for i in range(2):
    img = pg.image.load(f"player run{i}.png")
    player_run.append(img)

player_flip = []
for i in range(2):
    flip_img = pg.transform.flip((pg.image.load(f"player run{i}.png")),True, False)
    player_flip.append(flip_img)

opponent_run = []
for i in range(2):
    img = pg.image.load(f"opponent run{i}.png")
    opponent_run.append(img)

opponent_flip = []
for i in range(2):
    flip_img = pg.transform.flip((pg.image.load(f"opponent run{i}.png")),True, False)
    opponent_flip.append(flip_img)

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
    def __init__(self,x,y,w,h,opponent, run, flip):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.opponent = opponent
        self.run = run
        self.flip = flip
    
    def draw(b):
        screen.blit(b.run[1], (b.x,b.y))
        r = int(tick/3) % 2
        if opponent and ball.vy < 0:
            screen.blit(b.run[r], (b.x,b.y))
        if not opponent:
            if b.x > 0:
                screen.blit(b.run[r], (b.x,b.y))
            elif b.x < 0:
                screen.blit(b.flip[r], (b.x,b.y))
    
    def move(self, ball):
        if opponent and ball.vy < 0:
            self.x += (ball.x - self.x)/100
        if not opponent and ball.vy > 0:
            self.x += (ball.x - self.x)/100


ball = Ball(screen_w/2,screen_h/2,15)
opponent = Bro(screen_w/2,260,25,50,True, opponent_run, opponent_flip)
player = Bro(screen_w/2,550,50,100,False, player_run, player_flip)

background = pg.transform.scale(pg.image.load("tennisbane.png"),(screen_w,screen_h))

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
    tick += 1
    pg.display.flip()

pg.quit()