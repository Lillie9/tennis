import pygame as pg
import Reciever 
import random
import math


pg.font.init()

screen_w = 900
screen_h = 720

tick = 0
calibration_tick = 0

still_snit = 0
win_speed = -70

screen = pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption("Tennis")

# https://fonts.google.com/specimen/Press+Start+2P/about
text_size = 100
score_size = 50
font = pg.font.SysFont("bahnschrift", text_size)
score_font = pg.font.SysFont("bahnschrift",score_size )

player_size = 32 * 4
opponent_size = 32 * 3

ball_size = 90

score = False


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

ball_spin = []
for i in range(6):
    img = pg.image.load(f"ball{i}.png")
    img = pg.transform.scale(img,(ball_size, ball_size))
    ball_spin.append(img)

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
        q = int(tick/6) % 6
        screen.blit(ball_spin[q], (b.x,b.y))

    def move(b):
        b.x += b.vx/100
        b.y += b.vy/100
    
    def reset(b):
        b.x = screen_w/2
        b.y = screen_h/2
        b.vx = 0.5
        b.vy = 80

class Bro:
    def __init__(self,x,y,opponent, run):
        self.x = x
        self.y = y
        self.opponent = opponent
        self.run = run
        self.score = 0
    
    def draw(self, ball):
        r = int(tick/6) % 2
        if self.opponent and ball.vy <= 0:
            if ball.vx < 0:
                screen.blit(self.run[r], (self.x,self.y))
            else:
                screen.blit(pg.transform.flip(self.run[r], True, False), (self.x,self.y))
        elif self.opponent and ball.vy > 0:
            screen.blit(self.run[1], (self.x,self.y))
            
        if not self.opponent and ball.vy > 0:
            if ball.vx > 0:
                screen.blit(self.run[r], (self.x,self.y))
            else:
                screen.blit(pg.transform.flip(self.run[r], True, False), (self.x,self.y))
        elif not self.opponent and ball.vy < 0:
            screen.blit(self.run[1], (self.x,self.y))
    
    def move(self, ball):
        if self.opponent and ball.vy < 0:
            if ball.vx > 0:
                self.x += (ball.x - self.x)/100
            else:
                self.x += (ball.x - (self.x + player_size))/100
        
        if not self.opponent and ball.vy > 0:
            if ball.vx < 0:
                self.x += (ball.x - self.x)/100
            else:
                self.x += (ball.x - (self.x + player_size))/100

def draw_score(screen, playername, playerscore,x,y):   
    rendered_player = score_font.render(playername, True, (255,255,255))
    screen.blit(rendered_player, (x,y))
    text_width, text_height = score_font.size(playername)
    rendered_player_score = score_font.render(playerscore, True, (255,255,255))
    screen.blit(rendered_player_score, (x+text_width/2-score_font.size(playerscore)[0]/2,10+y+text_height))


ball = Ball(screen_w/2,screen_h/2,15)
opponent = Bro(screen_w/2,210,True, opponent_run)
player = Bro(screen_w/2,525,False, player_run)

background = pg.transform.scale(pg.image.load("tennisbane.png"),(screen_w,screen_h))
keyboard_slay = False
#Calibrating
while calibration_tick <= 120:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
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
        elif event.type  == pg.KEYUP:
            if event.key == pg.K_SPACE:
                keyboard_slay = False
        elif event.type  == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
       
            if event.key == pg.K_SPACE:
                keyboard_slay = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            print("mouse:", mouse_x, mouse_y)

    screen.blit(background,(0,0))

    #Movement
    data = Reciever.read()
    if data != None:
        x,y,z = data
        snit = (x + y + z)/3
        if snit > min_power or keyboard_slay :
            print("slay")
            if (player.y - ball.y) < 25 and (player.y - ball.y) > -50:
                if ball.vy > 0:
                    ball.vy *= -snit/100
                    vx_1 = int((ball.x - 208)/(696-272)*ball.vy)
                    vx_2 = int((ball.x - 685)/(696-272)*ball.vy)
                    print(vx_1, vx_2 )
  
                    ball.vx = random.randrange(vx_1,vx_2)
    
        
        if (ball.y - opponent.y) < 10 and ball.vy > win_speed:
            vx_1 = int((ball.x - 208)/(696-272)*ball.vy)
            vx_2 = int((ball.x - 685)/(696-272)*ball.vy)
            print(vx_1, vx_2)
            ball.vy *= -1
            ball.vx = random.randrange(vx_1,vx_2)

    #Check win    
    if (ball.y - player.y) > 75:
        opponent.score += 1
        ball.reset()
    
    if (ball.y - opponent.y) < -75:
        player.score += 1
        ball.reset()
        
        
    #print("player", player.score)  
    #print("opponent", opponent.score)
    playername = f"Player"
    playerscore = f"{player.score}"
    draw_score(screen, playername, playerscore,250,30)
    playername = f"Opponent"
    playerscore = f"{opponent.score}"
    draw_score(screen, playername, playerscore,487,30)
    

        

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