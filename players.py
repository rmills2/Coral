import pygame, sys, math, subprocess
from scratchpad import ScratchPad
from pygame.locals import *

############## Color Declarations ##############
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TAN= (247, 231, 160)

colorsArray = [GREEN, RED, BLUE, PURPLE, WHITE, YELLOW]

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getColor(self):
        return self.color
    def drawBox(self, display):
        pygame.draw.rect(display, self.getColor(), (self.getX() - 25, self.getY() - 25, 50, 50), 4)        
    def drawPlayerArrow(self, display, color, upArrow):
        if upArrow == False:
            pygame.draw.polygon(display, color, ((self.getX() - 2.5, 330), (self.getX() + 2.5, 330), (self.getX() + 2.5, 350), (7.5 + self.getX(), 350), (self.getX(), 360), (self.getX() - 7.5, 350), (self.getX() - 2.5, 350)))
            if color != TAN:
                pygame.draw.polygon(display, BLACK, ((self.getX() - 2.5, 330), (self.getX() + 2.5, 330), (self.getX() + 2.5, 350), (7.5 + self.getX(), 350), (self.getX(), 360), (self.getX() - 7.5, 350), (self.getX() - 2.5, 350)), 2)
            else:
                pygame.draw.polygon(display, color, ((self.getX() - 2.5, 330), (self.getX() + 2.5, 330), (self.getX() + 2.5, 350), (7.5 + self.getX(), 350), (self.getX(), 360), (self.getX() - 7.5, 350), (self.getX() - 2.5, 350)), 2)
        else:
            pygame.draw.polygon(display, color, ((self.getX() - 2.5, 490), (self.getX() + 2.5, 490), (self.getX() + 2.5, 470), (7.5 + self.getX(), 470), (self.getX(), 460), (self.getX() - 7.5, 470), (self.getX() - 2.5, 470)))
            if color != TAN:
                pygame.draw.polygon(display, BLACK, ((self.getX() - 2.5, 490), (self.getX() + 2.5, 490), (self.getX() + 2.5, 470), (7.5 + self.getX(), 470), (self.getX(), 460), (self.getX() - 7.5, 470), (self.getX() - 2.5, 470)), 2)
            else:
                pygame.draw.polygon(display, color, ((self.getX() - 2.5, 490), (self.getX() + 2.5, 490), (self.getX() + 2.5, 470), (7.5 + self.getX(), 470), (self.getX(), 460), (self.getX() - 7.5, 470), (self.getX() - 2.5, 470)), 2)

    

class PlayerArea:
    def __init__(self, players, display, x, y):
        self.players = players
        self.initialize(display, x, y)
    def getPlayers(self):
        return self.players
    def initialize(self, display, rectx, recty):
        pygame.draw.rect(display, TAN, (rectx, recty, 300, 180))
        pygame.draw.rect(display, BLACK, (rectx, recty, 300, 180), 4)
        x = rectx + 35
        y = recty + 65
        self.players = []
        for i in range(3):  
            self.players.append(Player(x, y, colorsArray[i]))
            pygame.draw.circle(display, colorsArray[i], (x, y), 15)
            if i == 2:
                x = rectx + 35
                y += 50
            else:
                x += 50
        pygame.draw.rect(display, (128, 128, 128), (770, 460, 130, 40))
        pygame.draw.rect(display, BLACK, (770, 460, 130, 40), 3)
        roomFont = pygame.font.SysFont("Times New Roman", 12)
        roomFont.set_bold(True)
        display.blit(roomFont.render("Make final", True, (255,255,255)), (800, 465))
        display.blit(roomFont.render("Accusation", True, WHITE), (800, 480))
        ## Create legend
        pygame.draw.rect(display, BLACK, (780, 330, 25, 25), 3)
        display.blit(roomFont.render("= Your Player", True, BLACK), (810, 335))
        pygame.draw.polygon(display, BLACK, ((790 - 2.5, 370), (790 + 2.5, 370), (790 + 2.5, 390), (7.5 + 790, 390), (790, 400), (790 - 7.5, 390), (790 - 2.5, 390)))
        display.blit(roomFont.render("= Active Player", True, BLACK), (805, 380))
