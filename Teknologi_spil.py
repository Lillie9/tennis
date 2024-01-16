import pygame as pg
import Reciever 
import random

pg.font.init()

screen_w = 900
screen_h = 720

tick = 0
calibration_tick = 0

still_snit = 0
win_speed = -200

screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("Tennis")

# https://fonts.google.com/specimen/Press+Start+2P/about
text_size = 100
font = pg.font.SysFont("bahnschrift", text_size)

player_size = 32 * 4
opponent_size = 32 * 3

player_run = []
for i in range(2):
    img = pg.image.load(f"player run{i}.png")
    img = pg.transform.scale(img,(player_size, player_size))
    player_run.append(img)

opponent_run = []
for i in range(2):
    img = pg.image.load(f"opponent run{i}.png")
    img = pg.transform.scale(img,(opponent_size, opponent_size))
    opponent_run.append(img)

clock = pg.time.Clock()
running = True

class Ball:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0.5
        self.vy = 80

    def draw(b):
        pg.draw.circle(screen, (230,230,0), (b.x,b.y), b.r)

    def move(b):
        b.x += b.vx/100
        b.y += b.vy/100

class Bro:
    def __init__(self,x,y,opponent, run):
        self.x = x
        self.y = y
        self.opponent = opponent
        self.run = run
    
    def draw(self, ball):
        r = int(tick/6) % 2
        if self.opponent and ball.vy <= 0:
            if ball.vx > 0:
                screen.blit(self.run[r], (self.x,self.y))
                print("opponent and ball.vy < 0")
            else:
                screen.blit(pg.transform.flip(self.run[r], True, False), (self.x,self.y))
                print(" opponent and ball.vy < 0 and ball.vx !< 0")
        elif self.opponent and ball.vy > 0:
            screen.blit(self.run[1], (self.x,self.y))
            print("opponent and ball.vy > 0")
            
        if not self.opponent and ball.vy > 0:
            if ball.vx < 0:
                screen.blit(self.run[r], (self.x,self.y))
                print("not opponent and ball.vy > 0")
            else:
                screen.blit(pg.transform.flip(self.run[r], True, False), (self.x,self.y))
                print("not opponent and ball.vy > 0 and ball.vx !< 0")
        elif not self.opponent and ball.vy < 0:
            screen.blit(self.run[1], (self.x,self.y))
            print("not opponent and ball.vy < 0")
    
    def move(self, ball):
        if self.opponent and ball.vy < 0:
            self.x += (ball.x - self.x)/100
        
        if not self.opponent and ball.vy > 0:
            self.x += (ball.x - self.x)/100


ball = Ball(screen_w/2,screen_h/2,15)
opponent = Bro(screen_w/2,210,True, opponent_run)
player = Bro(screen_w/2,525,False, player_run)

background = pg.transform.scale(pg.image.load("tennisbane.png"),(screen_w,screen_h))

#Calibrating
while calibration_tick <= 120:
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
    calibrating = font.render("Calibrating", True, (0,0,0))
    screen.blit(calibrating, (screen_w/2-250,screen_h/2-100))
    wait = font.render("Please wait", True, (0,0,0))
    screen.blit(wait, (screen_w/2-250,screen_h/2))

    data = Reciever.read()
    if data != None:
        x,y,z = data
        snit = (x + y + z)/3
        still_snit += snit
    else:
        continue
        
    
    clock.tick(60)
    calibration_tick += 1
    pg.display.flip()

still_snit = int(still_snit/120)
min_power = still_snit * 1.15

#Game loop
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
                    ball.vx *= (random.random() * 2 - 1) * 2
    
    if (ball.y - opponent.y) < 10 and ball.vy > win_speed:
        ball.vy *= -1
        ball.vx *= (random.random() * 2 - 1) * 25


    opponent.draw(ball)
    opponent.move(ball)
    ball.draw()
    ball.move()
    player.draw(ball)
    player.move(ball)

    clock.tick(60)
    tick += 1
    pg.display.flip()

pg.quit()