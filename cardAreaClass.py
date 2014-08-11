################Class cardArea#######################
import pygame, sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TAN= (247, 231, 160)

class cardArea:

    def __init__(self, display): ###draw card area###
        self.display = display
        cardAreaImg=pygame.image.load('cardArea.png')
        cardAreax=0
        cardAreay=500
        direction='right'
        display.blit(cardAreaImg,(cardAreax, cardAreay))
        
    def placeCards(self, cardList):
        myfont = pygame.font.SysFont("Times New Roman", 20)   
        x=44
        y=685
        i=0
        for i in range(len(cardList)):
            label = myfont.render(cardList[i], 1, BLACK)
            self.display.blit(label, (x, y))
            x+=141   

#############End of cardArea Class###################
