import pygame
import random
import math
import cv2
import apriltag
import numpy as np

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


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Paddle(pygame.sprite.Sprite):
    def __init__(self, up_key, down_key, xstart):
        super(Paddle, self).__init__()
        self.surf = pygame.Surface((10, 100))#(25, 250)
        self.surf.fill((0,0,0))
        self.surf.fill((255,255,255), self.surf.get_rect().inflate(-3, -3))
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
        self.surf.fill((0,0,0))
        self.surf.fill((255,255,255), self.surf.get_rect().inflate(-3, -3))        
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
        if self.rect.right >= SCREEN_WIDTH/2:
            self.rect.move_ip(-1,0)
        else:
            self.rect.move_ip(1,0)
        
        

screen= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(pygame.font.get_default_font(), 36)
raw_text = '0 | 0'
text = font.render(raw_text, True, (255,255,255), (0,0,0))
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH/2, 25)

dist = 100
#lpaddle = Paddle(K_w, K_s, dist)
#rpaddle = Paddle(K_UP, K_DOWN, SCREEN_WIDTH-dist-10)

#paddles = pygame.sprite.Group()
#paddles.add(lpaddle)
#paddles.add(rpaddle)

ball = Ball()

running = True

lscore=0
rscore=0

CAMERA_INDEX = 0

cap = cv2.VideoCapture(CAMERA_INDEX)
at_detector = apriltag.Detector()


while running:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    tags = at_detector.detect(cv2.flip(gray,1))

    
    all_corners = []
    if len(tags) > 0:
        for tag in tags[0:2]:
            corners = np.array(tag.corners, np.int32)
            for corner in corners:
                corner[0] = SCREEN_WIDTH - corner[0]
            

            """"""
            #            [(array([480, 222], dtype=int32), array([118,  94], dtype=int32)), (array([566, 383], dtype=int32), array([33, 29], dtype=int32))] <rect(328, 240, 10, 10)
                        
            all_corners.append(corners)
            cv2.polylines(frame, [corners], True, (0, 255, 0), thickness=3)



    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    bg = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB") #stackoverflow...
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.type == QUIT:
                running = False

    pressed_keys = pygame.key.get_pressed()
    #lpaddle.update(pressed_keys)
    #rpaddle.update(pressed_keys)

    screen.fill((0,0,0))
    screen.blit(bg, [0,0])
    #screen.blit(lpaddle.surf, lpaddle.rect)
    #screen.blit(rpaddle.surf, rpaddle.rect)
    
    screen.blit(ball.surf, ball.rect)

    
    screen.blit(text, textRect)

    

    if len(all_corners) > 0:
        tags=[]
        for i in range(len(all_corners)):
            tags.append((all_corners[i][0], all_corners[i][2]-all_corners[i][0]))
        print(tags, ball.rect)
        for i in range(len(tags)):
            if pygame.Rect(tags[i]).colliderect(ball.rect):
                print(i)
                ball.bounce_paddle()
        #if pygame.Rect(tags[0]).colliderect(ball.rect) or pygame.Rect(tags[1]).colliderect(ball.rect):

            #pygame.sprite.spritecollideany(ball, pygame.Rect(tag1)):
            #ball.bounce_paddle()
    #else:
    #    if pygame.sprite.spritecollideany(ball, paddles):
    #        ball.bounce_paddle()

        
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
