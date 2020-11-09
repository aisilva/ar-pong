import pygame
import random
import math
import cv2


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_s,
    K_w,    
    )

pygame.init()
clock = pygame.time.Clock()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700


class Paddle(pygame.sprite.Sprite):
    def __init__(self, up_key, down_key, xstart):
        super(Paddle, self).__init__()
        self.surf = pygame.Surface((10, 100))#(25, 250)
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.left = xstart
        
        self.up_key = up_key
        self.down_key = down_key
        
        self.speed = 6
        
    def update(self, pressed_keys):
        if pressed_keys[self.up_key]:
        #if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[self.down_key]:
        #if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)


        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


            
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.top = SCREEN_HEIGHT / 2
        self.rect.left = SCREEN_WIDTH / 2
        
        self.speed = 6
        #angle = 3.4
        #self.direction= [math.cos(angle), math.sin(angle)]
        self.direction = [1/math.sqrt(2), 1/math.sqrt(2)]

    def update(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction[1] = -self.direction[1]
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.direction[1] = -self.direction[1]

        if self.rect.left <= 0:
            self.rect.left = SCREEN_WIDTH/2
            self.direction[0] = -self.direction[0]
            #pts to rpaddle
            return -1

            
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH/2
            self.direction[0] = -self.direction[0]
            #pts to lpaddle
            return 1
            
        self.rect.move_ip(self.direction[0]*self.speed, self.direction[1]*self.speed)


    def bounce_paddle(self):
        angle = math.atan2(self.direction[0], -self.direction[1])# + 10*random.random()
        self.direction= [math.cos(angle), math.sin(angle)]
        
        

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(pygame.font.get_default_font(), 36)
raw_text = '0 | 0'
text = font.render(raw_text, True, (255,255,255), (0,0,0))
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH/2, 25)

dist = 100
lpaddle = Paddle(K_w, K_s, dist)
rpaddle = Paddle(K_UP, K_DOWN, SCREEN_WIDTH-dist-10)

paddles = pygame.sprite.Group()
paddles.add(lpaddle)
paddles.add(rpaddle)

ball = Ball()

running = True

lscore=0
rscore=0

#tux = cv2.imread('tux.jpeg')


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.type == QUIT:
                running = False

    pressed_keys = pygame.key.get_pressed()
    lpaddle.update(pressed_keys)
    rpaddle.update(pressed_keys)

    screen.fill((0,0,0))
    #screen.blit(tux, lpaddle.rect)
    screen.blit(lpaddle.surf, lpaddle.rect)
    screen.blit(rpaddle.surf, rpaddle.rect)
    screen.blit(ball.surf, ball.rect)

    
    screen.blit(text, textRect)

    
    if pygame.sprite.spritecollideany(ball, paddles):
        ball.bounce_paddle()

    score=ball.update()
    if score == 1:
        lscore+=1
        
        raw_text= str(lscore)+ ' | ' + str(rscore)
        
    elif score == -1:
        rscore+=1
        raw_text= str(lscore)+' | ' + str(rscore)
        
    text = font.render(raw_text, True, (255,255,255), (0,0,0))

    if lscore >= 11 or rscore >= 11:
        running = False
    
    pygame.display.flip()
    clock.tick(120)
