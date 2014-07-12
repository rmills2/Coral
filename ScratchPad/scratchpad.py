import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 700), 0, 32)
pygame.display.set_caption('Scratch Pad')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

myfont = pygame.font.SysFont("Times New Roman", 15)
text = myfont.render('Hello world!', True, WHITE, BLACK)
textRect = text.get_rect()
textRect.centerx = 100
textRect.centery = 100

def redrawRect(rect):
    pygame.draw.rect(DISPLAYSURF, WHITE, rect)
    pygame.draw.rect(DISPLAYSURF, BLACK, rect, 2)
def blitText(textName, rect):
    DISPLAYSURF.blit(myfont.render(textName, True, (0,0,0)), (150, rect.y))

weaponArray = ['Dagger', 'Rope', 'Lead Pipe', 'Candlestick', 'Revolver', 'Wrench']
roomArray = ['Kitchen', 'Ball Room', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge', 'Hall', 'Study']
peopleArray = ['Colonel Mustard', 'Professor Plum', 'Miss Scarlet', 'Mr. Green', 'Mrs. Peacock', 'Mrs. White']

allArray = peopleArray + weaponArray + roomArray
DISPLAYSURF.fill(WHITE)
colorsArray = []
def createAll(array):
    yVal = 0
    for i in range(len(allArray)):
        objectFromArray = allArray[i]
        colorsArray.append(True)
        r = pygame.Rect(0, yVal, 400, 20)
        pygame.draw.rect(DISPLAYSURF, BLACK, r, 2)
        blitText(objectFromArray, r)
        yVal += 20
pygame.display.update()

createAll(allArray)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            yVal = 0;
            for i in range(len(allArray)):
                r = pygame.Rect(0, yVal, 400, 20)
                if r.collidepoint(event.pos):
                    if colorsArray[i] == True:
                        pygame.draw.line(DISPLAYSURF, RED, (0, yVal + 10), (400, yVal + 10), 3)
                        colorsArray[i] = False;
                    else:
                        redrawRect(r)
                        blitText(allArray[i], r)
                        colorsArray[i] = True
                yVal += 20                  
    pygame.display.update()
