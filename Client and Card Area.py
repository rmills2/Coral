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


############Client Class#################

class Client:
    
    randomNumber1=(randint(0,5))
    randomNumber2=(randint(0,5))
    nameArray=["Miss Scarlet", "Prof. Plum", "Mrs. Peacock", "Mr. Green", "Mrs. White", "Col. Mustard"]
    colorArray=[WHITE, BLACK, BLUE, GREEN, RED, YELLOW]
    name="a"
    color=RED
    cardArray=["1","2","3","4","5","6"]
    cardCounter=0

    def _init_(self):
        self.setName()
        self.setColor()
        
    def setName(self):
        self.name=self.nameArray[self.randomNumber1]

    def getName(self):
        return self.name

    def setColor(self):
        self.color=self.colorArray[self.randomNumber2]   ######## Why not randomnized?  ########

    def getColor(self):
        return self.color

    def setCard(self, cardName1, cardName2, cardName3, cardName4, cardName5, cardName6):
        self.cardArray=[cardName1, cardName2, cardName3, cardName4, cardName5, cardName6]
        i=0
        while (self.cardArray[i]!="" and i<=5):
            self.cardCounter+=1
            i+=1
            
    def getCard(self):
        return self.cardArray


###########cardArea Class#################    
class cardArea:

    
    def placeCards(self,getattr(Client,'cardArray'))    ############## how to call method from another object##
    i=0
    while i<=5:
        x=40
        y=180
        lable=myfont.render(getattr(Client,cardArray[i]),1, BLACK)
        screen.blit(label, (x, y))
        x+=150
    



while True: # the main game loop
    DISPLAYSURF.fill(WHITE)

    
    DISPLAYSURF.blit(cardAreaImg,(cardAreax, cardAreay))

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
    
