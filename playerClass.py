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




############Player Class#################

class Player:
    
    
    nameArray=["Miss Scarlet", "Prof. Plum", "Mrs. Peacock", "Mr. Green", "Mrs. White", "Col. Mustard"]
    colorArray=[WHITE, BLACK, BLUE, GREEN, RED, YELLOW, PURPLE, TAN]
    name="a"
    color=RED
    cardArray=["1","2","3","4","5","6"]
    cardCounter=0

    def _init_(self):
        self.setName()
        self.setColor()
        
    def setName(self):
        randomNumber=(randint(0,5))
        self.name=self.nameArray[randomNumber]

    def getName(self):
        return self.name

    def setColor(self):
        randomNumber=(randint(0,7))
        self.color=self.colorArray[randomNumber]

    def getColor(self):
        return self.color
    
    def setCard(self, list):
        self.cardArray=list
        i=0
        while (self.cardArray[i]!="" and i<=5):
            self.cardCounter+=1
            i+=1
            
    def getCard(self):
        return self.cardArray

#############End of Client Class#######################




while True: # the main game loop

    myfont = pygame.font.SysFont("Times New Roman", 50)


#########test functionality#############    
    cardArray=['Mr. Plum', 'Rope', 'Ms. Scarlet','Lounge','Mrs. Peacock','']
    a=Player()
    a.setCard(cardArray)
    a.setName()
    a.setColor()
    print a.getName(),a.getColor()
    print a.getCard()
    print 'Number of cards this player has:', a.cardCounter
    break
    
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)

    
    

