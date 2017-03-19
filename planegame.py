#-*-coding:utf-8-#-
import pygame
import random
from sys import exit

def checkhit(enemy,bullet):
    if(bullet.x>enemy.x and bullet.x<enemy.x+enemy.image.get_width())and(bullet.y>enemy.y and bullet.y<enemy.y+enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    return False

def checkcrash(enemy,plane):
    if (plane.x + 0.7*plane.image.get_width()>enemy.x)and(plane.x+0.3*plane.image.get_width()<enemy.x+enemy.image.get_width())and(plane.y+0.7*plane.image.get_height()>enemy.y)and(plane.y+0.3*plane.image.get_height()<enemy.y+enemy.image.get_height()):
        return True
    return False
        
class Plane:
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()
    def restart(self):
        self.x = 200
        self.y = 500
    def move(self):
        x,y = pygame.mouse.get_pos()
        x -= self.image.get_width()/2
        y -= self.image.get_height()/2
        self.x = x
        self.y = y
     
class Enemy:
    def __init__(self):
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.restart()
    def move(self):
        if self.y < 600:
            self.y += self.speed
        else:
            self.y = -50
            self.restart()
    def restart(self):
        self.x = random.random()*400
        self.y = random.randint(-500,-50)
        self.speed = random.random()/3.5+0.1
        
class Bullet:
    def __init__(self):
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.x = 0
        self.y = -1
        self.active = False
    def move(self):
        if self.active:
            self.y -= 6
        if self.y < 0:
            self.active = False
    def restart(self):
        mousex,mousey = pygame.mouse.get_pos()
        self.x = mousex - self.image.get_width()/2
        self.y = mousey - self.image.get_height()/2
        self.active = True
            
pygame.init()        
screen = pygame.display.set_mode((450,600),0,32)
pygame.display.set_caption('飞机可不能乱打哦~')
background = pygame.image.load('back.jpg').convert()
plane = Plane()

bullets = []
for i in range(5):
    bullets.append(Bullet())
count_b = len(bullets)
index_b = 0
interval_b = 0

enemys = []
for i in range(8):
    enemys.append(Enemy())
    
gameover = False
score = 0
font = pygame.font.Font(None,32)
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if gameover and event.type == pygame.MOUSEBUTTONUP:
                plane.restart()
                for e in enemys:
                    e.restart()
                for b in bullets:
                    b.active = False
                score = 0
                gameover = False
        screen.blit(background,(0,0))
        if not gameover:
            interval_b -= 1
            if interval_b < 0:
                bullets[index_b].restart()
                interval_b = 100
                index_b = (index_b+1) % count_b
            for b in bullets:
                if b.active:
                    for e in enemys:
                        if checkhit(e,b):
                            score += 100
                    b.move()
                    screen.blit(b.image,(b.x,b.y))
            for e in enemys:
                if checkcrash(e,plane):
                    gameover = True
                    text = font.render('Score:%d' % score,1,(0,0,0))
                    screen.blit(text,(150,150))
                e.move()
                screen.blit(e.image,(e.x,e.y))
            plane.move()
            screen.blit(plane.image,(plane.x,plane.y))
            pygame.display.update()

