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
        x = rectx + 100
        y = recty + 65
        self.players = []
        for i in range(6):  
            self.players.append(Player(x, y, colorsArray[i]))
            pygame.draw.circle(display, colorsArray[i], (x, y), 15)
            if i == 2:
                x = rectx + 100
                y += 50
            else:
                x += 50
