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


############## Game and Font Initialization ###############
pygame.init()
display = pygame.display.set_mode((900, 600), 0, 32)
pygame.display.set_caption('Board')
myfont = pygame.font.SysFont("Times New Roman", 50)
display.fill(WHITE)


############## Scratch Pad Integration ################

scratchColorsArray = []
allArray = []
scratchPad = ScratchPad(display, scratchColorsArray, allArray)
allArray = scratchPad.runScratchPad()

############## Internal Class Declarations ##############
class Character:
    def __init__(self, name, color, currentSpace):
        self.name = name
        self.color = color
        self.currentSpace = currentSpace
    def name(self):
        return self.name
    def color(self):
        return self.color
    def draw(self):
        pygame.draw.circle(display, self.color, (self.currentSpace.x + 60, self.currentSpace.y + 60), 15)
    def currentSpace(self):
        return self.currentSpace

class Space:
    def __init__(self, x, y, maxOccupancy, currentOccupants):
        self.x = x
        self.y = y
        self.maxOccupancy = maxOccupancy
        self.currentOccupants = currentOccupants
    def x(self):
        return self.x
    def y(self):
        return self.y
    def maxOccupancy(self):
        return self.maxOccupancy
    def currentOccupants(self):
        return self.currentOccupants

class Hallway(Space):
    def __init__(self, x, y, maxOccupancy, currentOccupants, vertical):
        Space.__init__(self, x, y, maxOccupancy, currentOccupants)
        self.vertical = vertical
    def vertical(self):
        return self.vertical
    def draw(self):
        if self.vertical == True:              
            rect = pygame.Rect(self.x + 30, self.y, 60, 120)
            drawRect(rect, BLACK, "")
        else:
            rect = pygame.Rect(self.x, self.y + 30, 120, 60)
            drawRect(rect, BLACK, "")

class Room(Space):
    def __init__(self, x, y, maxOccupancy, currentOccupants, name, image):
        Space.__init__(self, x, y, maxOccupancy, currentOccupants)
        self.name = name
        self.image = image
    def name(self):
        return self.name
    def image(self):
        return self.image

class SpecialRoom(Room):
    def __init__(self, x, y, maxOccupancy, currentOccupants, name, image, secretPassageSpot):
        Room.__init__(self, x, y, maxOccupancy, currentOccupants, name, image)
        self.secretPassageSpot = secretPassageSpot
    def secretPassageSpot(self):
        return self.secretPassageSpot


############## Create global arrays ###############

images = ['study.jpg', 'hall.jpg', 'lounge.jpg', 'library.jpg', 'billiardRoom.jpg', 'diningRoom.jpg', 'conservatory.jpg', 'ballroom.jpg', 'kitchen.jpg']
roomArray = ['1','2','3','4','5','6','7','8','9']
characters = ['Player1', 'Player2', 'Player3', '4', '5']
colorsArray = [GREEN, RED, BLUE, PURPLE, WHITE, YELLOW]


############## Global Variable Declarations ###############
x = 0
y = 0
characterArray = []
color = BLACK
arrayCount = 0
spotArray = []
specialRooms = []
colorCount = 0


############## Utility Methods #################

def redrawRect(rect):
    pygame.draw.rect(display, WHITE, rect)
    pygame.draw.rect(display, BLACK, rect, 2)
def undrawCircle(character, spotArray):
    currentSpace = character.currentSpace
    color = BLACK
    if isinstance(currentSpace, Room):
        display.blit(currentSpace.image, (currentSpace.x, currentSpace.y))
        for i in range(len(currentSpace.currentOccupants)):
            char = currentSpace.currentOccupants[i]
            if char != character:
                char.draw()
    else:
        pygame.draw.circle(display, color, (character.currentSpace.x + 60, character.currentSpace.y + 60), 15)
def drawRect(rect, color, text):
    pygame.draw.rect(display, color, rect)
def drawCircle(rect, color):
    pygame.draw.circle(display, color, (rect.centerx, rect.centery), 15)

def spaceAt(spotArray, x, y):
    for i in range(len(spotArray)):
        spot = spotArray[i]
        if spot.x == x and spot.y == y:
            return spot
def getValidSpaces(spot, spotArray):
    validSpaces = []
    for i in range(len(spotArray)):
        if (((spot.x + 120 == spotArray[i].x or spot.x - 120 == spotArray[i].x) and (spot.y == spotArray[i].y)) or ((spot.y + 120 == spotArray[i].y or spot.y - 120 == spotArray[i].y) and (spot.x == spotArray[i].x))):
            validSpaces.append(spotArray[i])
    return validSpaces
def drawCharactersInSpace(characters, space):
    scalex = 20
    scaley = 20

    spaceColor = YELLOW
    if isinstance(space, Room):
        spaceColor = BLACK

    rect = pygame.Rect(space.x, space.y, 120, 120)
    if isinstance (space, Room):
        display.blit(space.image, (rect.x, rect.y))
    else:
        drawRect(rect, spaceColor, "")
        
    for i in range(len(characters)):
        pygame.draw.circle(display, characters[i].color, (space.x + scalex, space.y + scaley), 15)
        characters[i].x = space.x + scalex
        characters[i].y = space.y + scaley
        if scalex > 60:
            scalex = 20
            scaley += 32
        else:
            scalex += 32

def isAdjacent(space, spots, characterSpace):
    if space not in getValidSpaces(characterSpace, spotArray):
        print "Not adjacent!"
        return False
    else:
        return True

def isValidSecretPassage(spaceToGo, characterSpace):
    if isinstance(spaceToGo, SpecialRoom) and isinstance(characterSpace, SpecialRoom) and characterSpace.secretPassageSpot == spaceToGo:
        return True
    return False

############## Main Loop to create Rooms and Characters ##############
for i in range(5):
    x = 0
    for j in range(5):
        rect = pygame.Rect(x * 10, y * 10, 120, 120)
        if (i ==0 or i == 2 or i == 4) and (j == 0 or j == 2 or j == 4):            
            drawRect(rect, color, roomArray[arrayCount])
            currentImage = pygame.transform.scale(pygame.image.load('resources/images/' + images[arrayCount]), (120, 120))
            display.blit(currentImage, (rect.x, rect.y))
            
            arrayCount+= 1
            if (i == 0 and j == 0) or (i == 0 and j ==4) or (i == 4 and j == 0) or (i == 4 and j == 4):
                specialRoom = SpecialRoom(rect.x, rect.y, 6, [], "Special Room", currentImage, [])
                spotArray.append(specialRoom)
                specialRooms.append(specialRoom)
            else:
                spotArray.append(Room(rect.x, rect.y, 6, [], "Room", currentImage))
        else:
            hallway = []
            drawRect(rect, TAN, "No Room")
            if i%2 == 1 and j%2 == 0:
                hallway = Hallway(rect.x, rect.y, 1, [], True)
                hallway.draw()
                spotArray.append(hallway)
            elif i%2 == 0 and j%2 == 1:
                hallway = Hallway(rect.x, rect.y, 1, [], False)
                hallway.draw()
                spotArray.append(hallway)
        if (j == 0 and i % 2 == 1) or (i == 4 and j % 2 == 1) or (j == 4 and i == 1) or (i == 0 and j == 1):
            character = Character(characters[i], colorsArray[colorCount], spaceAt(spotArray, rect.x, rect.y))
            character.draw()
            colorCount += 1
            space = character.currentSpace
            space.currentOccupants.append(character)
            characterArray.append(character)
        x += 12
    y += 12

############## Associate Special Rooms ##################
for i in range(len(specialRooms)):
    for j in range(len(specialRooms)):
        spA = specialRooms[i]
        spB = specialRooms[j]
        if (spA != spB and spA.x != spB.x and spA.y != spB.y and spA.secretPassageSpot == []):
            spA.secretPassageSpot = spB
            spB.secretPassageSpot = spA
            

############### Main Game Loop for Game-Play Interaction #################
turn = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(spotArray)):
                rect = pygame.Rect(spotArray[i].x, spotArray[i].y, 120, 120)
                if rect.collidepoint(event.pos):
                   currentCharacter = characterArray[turn % len(characterArray)]
                   characterRect = pygame.Rect(currentCharacter.currentSpace.x, currentCharacter.currentSpace.y, 120, 120)
                   if isValidSecretPassage(spotArray[i], currentCharacter.currentSpace) == False and isAdjacent(spotArray[i], spotArray, currentCharacter.currentSpace) == False or spotArray[i].maxOccupancy - len(spotArray[i].currentOccupants) <= 0:
                       #### Insert popup message with incorrect spot #####
                       break
                   else:
                       undrawCircle(currentCharacter, spotArray)
                       turn += 1                      
                       currentCharacter.x = rect.x + 60
                       currentCharacter.y = rect.y + 60
                       currentCharacter.currentSpace.currentOccupants.remove(currentCharacter)
                       currentCharacter.currentSpace = spotArray[i]
                       currentCharacter.currentSpace.currentOccupants.append(currentCharacter)
                       if isinstance(spotArray[i], Room):
                           drawCharactersInSpace(spotArray[i].currentOccupants, spotArray[i])
                           print "Would you like to make an accusation?"
                       else:
                            drawCircle(rect, currentCharacter.color)
            yVal = 0

            ##### Checks for scratch pad #####
            for i in range(len(allArray)):
                r = pygame.Rect(600, yVal, 300, 20)
                if r.collidepoint(event.pos):
                    if scratchPad.scratchColorsArray[i] == True:
                        pygame.draw.line(display, RED, (600, yVal + 10), (900, yVal + 10), 3)
                        scratchPad.scratchColorsArray[i] = False;
                    else:
                        redrawRect(r)
                        ScratchPad.blitText(allArray[i], r, display)
                        scratchPad.scratchColorsArray[i] = True
                yVal += 20
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
