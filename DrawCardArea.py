import pygame, sys, math, subprocess
from pygame. locals import *
from random import randint

pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TAN= (247, 231, 160)



# frames per second setting

FPS=30 
fpsClock=pygame.time.Clock()

############## Game and Font Initialization ###############
DISPLAYSURF=pygame.display.set_mode((900, 800), HWSURFACE|DOUBLEBUF)
pygame.display.set_caption('Board')
myfont = pygame.font.SysFont("Times New Roman", 50)
roomFont = pygame.font.SysFont("Times New Roman", 15)
roomFont.set_bold(True)


#Load cardArea Image
cardAreaImg=pygame.image.load('cardArea.png')
cardAreax=0
cardAreay=600
direction='right'


while True: # the main game loop
    DISPLAYSURF.fill(WHITE)

    
    DISPLAYSURF.blit(cardAreaImg,(cardAreax, cardAreay))

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
    



