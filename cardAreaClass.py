################Class cardArea#######################

class cardArea:

    def _init_(self): ###draw card area###
        cardAreaImg=pygame.image.load('cardArea.png')
        cardAreax=0
        cardAreay=500
        direction='right'
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(cardAreaImg,(cardAreax, cardAreay))
        
    def placeCards(self, list):
        myfont = pygame.font.SysFont("Times New Roman", 20)
        cardArray=list    
        x=44
        y=685
        i=0
        while i<=5:
            label = myfont.render(cardArray[i], 1, BLACK)
            DISPLAYSURF.blit(label, (x, y))
            x+=141
            i+=1    

#############End of cardArea Class###################




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


#Load cardArea Image#


        
while True: # the main game loop#


##########create cardArea object and draw cardArea####
    x=cardArea()
    x._init_()

###########Place Cards on cardArea#################
    cardArray=['Mr. Plum', 'Rope', 'Ms. Scarlet','Lounge','Mrs. Peacock','']
    x.placeCards(cardArray)

    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
