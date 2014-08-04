import pygame, sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK= (0, 0, 0)
TAN= (247, 231, 160)
RED = (255, 0, 0)
#pygame.init()
#display = pygame.display.set_mode((900, 500), HWSURFACE|DOUBLEBUF)
#pygame.display.set_caption('Board')

class Entry:
    def __init__(self, rect, name):
        self.rect = rect
        self.name = name
    def getRect(self):
        return self.rect
    def getName(self):
        return self.name

entries = []

class ScratchPad:
    def __init__(self, display, scratchColorsArray, allArray):
        weaponArray = ['Dagger', 'Rope', 'Lead Pipe', 'Candlestick', 'Revolver', 'Wrench']
        roomArray = ['Kitchen', 'Ball Room', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge', 'Hall', 'Study']
        peopleArray = ['Colonel Mustard', 'Professor Plum', 'Miss Scarlet', 'Mr. Green', 'Mrs. Peacock', 'Mrs. White']
        self.display = display
        self.scratchColorsArray = scratchColorsArray
        self.allArray = allArray
        self.peopleArray = peopleArray
        self.weaponArray = weaponArray
        self.roomArray = roomArray
    def runScratchPad(self):
        myfont = pygame.font.SysFont("Times New Roman", 15)
        myfont.set_bold(True)
        text = myfont.render('Hello world!', True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.centerx = 700
        textRect.centery = 100
        self.display.fill(TAN)
        return self.createAll()
    @staticmethod
    def blitText(textName, rect, display):
        myfont = pygame.font.SysFont("Times New Roman", 15)
        myfont.set_bold(True)
        display.blit(myfont.render(textName, True, (0,0,0)), (rect.x + 2, rect.y))
    def createAll(self):
        yVal = 20
        pygame.draw.rect(self.display, BLACK, (600, 0, 300, 500), 4)
        rect = pygame.Rect(610, 10, 120, 20)
        ScratchPad.blitText("Suspects", rect, self.display)
        self.allArray = []
        myArray = []
        for i in range(len(self.peopleArray)):
            obj = self.peopleArray[i]
            self.scratchColorsArray.append(True)
            r = pygame.Rect(610, 10 + yVal, 120, 20)
            pygame.draw.rect(self.display, BLACK, r, 2)
            ScratchPad.blitText(obj, r, self.display)
            yVal += 20
            print self.peopleArray[i]
            entries.append(Entry(r, self.peopleArray[i]))

        r = pygame.Rect(610, 30 + yVal, 120, 20)
        ScratchPad.blitText("Weapons", r, self.display)
        for i in range(len(self.weaponArray)):
            obj = self.weaponArray[i]
            self.scratchColorsArray.append(True)
            r = pygame.Rect(610, 50 + yVal, 120, 20)
            pygame.draw.rect(self.display, BLACK, r, 2)
            ScratchPad.blitText(obj, r, self.display)
            yVal += 20
            print self.weaponArray[i]
            entries.append(Entry(r, self.weaponArray[i]))

        yVal = 90
        r = pygame.Rect(750, yVal - 10, 120, 20)
        ScratchPad.blitText("Rooms", r, self.display)
        for i in range(len(self.roomArray)):
            obj = self.roomArray[i]
            self.scratchColorsArray.append(True)
            r = pygame.Rect(750, 10 + yVal, 120, 20)
            pygame.draw.rect(self.display, BLACK, r, 2)
            ScratchPad.blitText(obj, r, self.display)
            yVal += 20
            print self.roomArray[i]
            entries.append(Entry(r, self.roomArray[i]))
        pygame.display.update()
        return entries
    def redrawEntryArea(self, display, rect):
        pygame.draw.rect(display, TAN, rect)
        pygame.draw.rect(display, BLACK, rect, 2)
