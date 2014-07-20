import pygame, sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK= (0, 0, 0)

class ScratchPad:
    def __init__(self, display, scratchColorsArray, allArray):
        weaponArray = ['Dagger', 'Rope', 'Lead Pipe', 'Candlestick', 'Revolver', 'Wrench']
        roomArray = ['Kitchen', 'Ball Room', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge', 'Hall', 'Study']
        peopleArray = ['Colonel Mustard', 'Professor Plum', 'Miss Scarlet', 'Mr. Green', 'Mrs. Peacock', 'Mrs. White']
        allArray = peopleArray + weaponArray + roomArray
        self.display = display
        self.scratchColorsArray = scratchColorsArray
        self.allArray = allArray
    def runScratchPad(self):
        myfont = pygame.font.SysFont("Times New Roman", 15)
        text = myfont.render('Hello world!', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.centerx = 700
        textRect.centery = 100
        self.display.fill(WHITE)
        self.createAll()
        return self.allArray
    @staticmethod
    def blitText(textName, rect, display):
        myfont = pygame.font.SysFont("Times New Roman", 15)
        display.blit(myfont.render(textName, True, (0,0,0)), (rect.x + 150, rect.y))
    def createAll(self):
        yVal = 0
        for i in range(len(self.allArray)):
            objectFromArray = self.allArray[i]
            self.scratchColorsArray.append(True)
            r = pygame.Rect(600, yVal, 300, 20)
            pygame.draw.rect(self.display, BLACK, r, 2)
            ScratchPad.blitText(objectFromArray, r, self.display)
            yVal += 20
        pygame.display.update()
