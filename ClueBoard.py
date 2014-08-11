import pygame, sys, math, subprocess
from scratchpad import ScratchPad
from client import *
from Message import *
from players import *
from cardAreaClass import *
from pygame.locals import *
import sys

############## Color Declarations ##############
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TAN= (247, 231, 160)

############## Initialize Client ###############
#client = ClueLessClient(ConnectionListener)


############## Game and Font Initialization ###############
pygame.init()
display = pygame.display.set_mode((900, 800), HWSURFACE|DOUBLEBUF)
pygame.display.set_caption('Board')
myfont = pygame.font.SysFont("Times New Roman", 50)
roomFont = pygame.font.SysFont("Times New Roman", 15)
roomFont.set_bold(True)
display.fill(TAN)

############## Scratch Pad Integration ################

scratchColorsArray = []
allArray = []
scratchPad = ScratchPad(display, scratchColorsArray, allArray)
entries = scratchPad.runScratchPad()


############## Player Area Integration ################
playerArea = PlayerArea([], display, 600, 320)


############## Card Area Initialization ##############
cardArea = cardArea(display)
#myCards = ['Wrench', 'Prof. Plum', 'Col. Mustard', 'Mrs. White'] # cards should come from server
myCards = sys.argv[1].split(",") if len(sys.argv) > 1 else ['Wrench', 'Prof. Plum', 'Col. Mustard', 'Mrs. White']# cards should come from server
cardArea.placeCards(myCards) 


############## Internal Class Declarations ##############
class GameBoard:
    def __init__(self, cardAreaCards, player, playerId):
        self.cardAreaCards = cardAreaCards
        self.player = player
        self.playerId = playerId
    def getCardAreaCards(self):
        return self.cardAreaCards
    def getPlayer(self):
        return self.player
    def getPlayerId(self):
        return self.playerId
    
class Character:
    def __init__(self, name, color, currentArea):
        self.name = name
        self.color = color
        self.currentArea = currentArea
    def name(self):
        return self.name
    def color(self):
        return self.color
    def draw(self):
        scalex = 20
        scaley = 50
        area = self.currentArea
        characters = area.currentOccupants
        areaColor = YELLOW
        if isinstance(area, Room):
            areaColor = TAN
            rect = pygame.Rect(area.x, area.y, 120, 100)
            Area.draw(rect, areaColor)
            if isinstance (area, Room):    
                display.blit(area.image, (rect.x, rect.y))               
                display.blit(roomFont.render(area.name, True, (255,255,255)), (rect.x + 10, rect.y + 75))
                for i in range(len(characters)):
                    pygame.draw.circle(display, characters[i].color, (rect.x + scalex, rect.y + scaley), 15)
                    characters[i].x = rect.x + scalex
                    characters[i].y = rect.y + scaley
                    if scalex > 60:
                        scalex = 20
                        scaley += 32
                    else:
                        scalex += 32
        else:
            area.draw()
            pygame.draw.circle(display, self.color, (area.x + 60, area.y + 60), 15)
        
    def currentArea(self):
        return self.currentArea
    def moveCharacter(self, newArea):
        currentArea = self.currentArea
        currentArea.currentOccupants.remove(self)
        self.currentArea = newArea
        self.currentArea.currentOccupants.append(self)
        color = BLACK
        if isinstance(currentArea, Room):
            display.blit(currentArea.image, (currentArea.x, currentArea.y))
            if len(currentArea.currentOccupants) == 0:              
                display.blit(roomFont.render(currentArea.name, True, (255,255,255)), (currentArea.x + 10, currentArea.y + 75))
            for i in range(len(currentArea.currentOccupants)):
                char = currentArea.currentOccupants[i]
                if char != self:
                    char.draw()
        else:
            pygame.draw.circle(display, color, (currentArea.x + 60, currentArea.y + 60), 15)

class Area:
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
    
    @staticmethod
    def draw(rect, color):
        pygame.draw.rect(display, color, rect)
    
    def isAdjacent(self, spots, characterArea):
        if self not in self.getValidAreas(characterArea, spots):
            print "Not adjacent!"
            return False
        else:
            return True
    def getValidAreas(self, spot, spotArray):
        validAreas = []
        for i in range(len(spotArray)):
            if (((spot.x + 120 == spotArray[i].x or spot.x - 120 == spotArray[i].x) and (spot.y == spotArray[i].y)) or ((spot.y + 100 == spotArray[i].y or spot.y - 100 == spotArray[i].y) and (spot.x == spotArray[i].x))):
                validAreas.append(spotArray[i])
        return validAreas

class Hallway(Area):
    def __init__(self, x, y, maxOccupancy, currentOccupants, vertical):
        Area.__init__(self, x, y, maxOccupancy, currentOccupants)
        self.vertical = vertical
    def vertical(self):
        return self.vertical
    def draw(self):
        if self.vertical == True:              
            rect = pygame.Rect(self.x + 30, self.y, 60, 100)
            Area.draw(rect, BLACK)
        else:
            rect = pygame.Rect(self.x, self.y + 30, 120, 50)
            Area.draw(rect, BLACK)

class Room(Area):
    def __init__(self, x, y, maxOccupancy, currentOccupants, name, image):
        Area.__init__(self, x, y, maxOccupancy, currentOccupants)
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

images = ['study.png', 'hall.png', 'lounge.png', 'library.png', 'billiardRoom.png', 'diningRoom.png', 'conservatory.png', 'ballroom.png', 'kitchen.png']
roomArray = ['Study','Hall','Lounge','Library','Billiard Room','Dining Room','Conservatory','Ballroom','Kitchen']
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

def areaAt(spotArray, x, y):
    for i in range(len(spotArray)):
        spot = spotArray[i]
        if spot.x == x and spot.y == y:
            return spot

def isValidSecretPassage(areaToGo, characterArea):
    if isinstance(areaToGo, SpecialRoom) and isinstance(characterArea, SpecialRoom) and characterArea.secretPassageSpot == areaToGo:
        return True
    return False


############## Main Loop to create Rooms and Characters ##############
for i in range(5):
    x = 0
    for j in range(5):
        rect = pygame.Rect(x * 10, y * 10, 120, 100)
        if (i ==0 or i == 2 or i == 4) and (j == 0 or j == 2 or j == 4):
            Area.draw(rect, TAN)
            currentImage = pygame.transform.scale(pygame.image.load('resources/images/' + images[arrayCount]), (120, 100)).convert_alpha()
            display.blit(currentImage, (rect.x, rect.y))
            display.blit(roomFont.render(roomArray[arrayCount], True, (255,255,255)), (rect.x + 10, rect.y + 75))
            
            if (i == 0 and j == 0) or (i == 0 and j ==4) or (i == 4 and j == 0) or (i == 4 and j == 4):
                specialRoom = SpecialRoom(rect.x, rect.y, 6, [], roomArray[arrayCount], currentImage, [])
                spotArray.append(specialRoom)
                specialRooms.append(specialRoom)
            else:
                spotArray.append(Room(rect.x, rect.y, 6, [], roomArray[arrayCount], currentImage))

            arrayCount+= 1
        else:
            hallway = []
            Area.draw(rect, TAN)
            if i%2 == 1 and j%2 == 0:
                hallway = Hallway(rect.x, rect.y, 1, [], True)
                hallway.draw()
                spotArray.append(hallway)
            elif i%2 == 0 and j%2 == 1:
                hallway = Hallway(rect.x, rect.y, 1, [], False)
                hallway.draw()
                spotArray.append(hallway)
        if (j == 0 and i % 2 == 1) or (i == 4 and j % 2 == 1) or (j == 4 and i == 1) or (i == 0 and j == 1):
            character = Character(characters[i], colorsArray[colorCount], areaAt(spotArray, rect.x, rect.y))
            colorCount += 1
            area = character.currentArea
            area.currentOccupants.append(character)
            characterArray.append(character)
            character.draw()
        x += 12
    y += 10

############## Associate Special Rooms ##################
for i in range(len(specialRooms)):
    for j in range(len(specialRooms)):
        spA = specialRooms[i]
        spB = specialRooms[j]
        if (spA != spB and spA.x != spB.x and spA.y != spB.y and spA.secretPassageSpot == []):
            spA.secretPassageSpot = spB
            spB.secretPassageSpot = spA
    

############### Draw Border ###################
pygame.draw.rect(display, BLACK, (0, 0, 600, 500), 4)


############### Main Game Loop for Game-Play Interaction #################
turn = 0
youAre = 2
playerArea.players[turn].drawPlayerArrow(display, playerArea.players[turn].getColor(), False)
playerArea.players[youAre].drawBox(display)

############## Create Message ###################
#create_message("start", [])

while True:
    for event in pygame.event.get():
        #if turn == youAre:
            #create_message("move")
        if event.type == pygame.MOUSEBUTTONUP:
            #if GameBoard.getPlayerId == client.turn:
                for i in range(len(spotArray)):
                    rect = pygame.Rect(spotArray[i].x, spotArray[i].y, 120, 100)
                    if rect.collidepoint(event.pos):
                       currentCharacter = characterArray[turn % len(characterArray)]
                       characterRect = pygame.Rect(currentCharacter.currentArea.x, currentCharacter.currentArea.y, 120, 100)
                       if isValidSecretPassage(spotArray[i], currentCharacter.currentArea) == False and spotArray[i].isAdjacent(spotArray, currentCharacter.currentArea) == False or spotArray[i].maxOccupancy - len(spotArray[i].currentOccupants) <= 0:
                           create_message("invalidMove")
                           break
                       else:
                           currentCharacter.moveCharacter(spotArray[i])
                           
                            ##### Update the player area
                           previousPlayer = playerArea.players[turn % len(playerArea.players)]
                           if turn % len(playerArea.players) == 2:
                               previousPlayer.drawPlayerArrow(display, TAN, False)
                           elif turn % len(playerArea.players) == 5:
                               previousPlayer.drawPlayerArrow(display, TAN, True)
                           turn += 1
                           currentPlayer = playerArea.players[turn % len(playerArea.players)]
                
                           if turn % len(playerArea.players) > 2:
                               previousPlayer.drawPlayerArrow(display, TAN, True)
                               currentPlayer.drawPlayerArrow(display, currentPlayer.getColor(), True)
                           else:
                               previousPlayer.drawPlayerArrow(display, TAN, False)
                               currentPlayer.drawPlayerArrow(display, currentPlayer.getColor(), False)
                           if isinstance(spotArray[i], Room):
                               currentCharacter.draw()
                               pygame.display.update()
                               ### This would be a prompt instead
                               ## for Player in Players
                               ## if Player == "PlayerFromCard"
                               ## draw player at spot as well to move them there
                               cards="Dagger,Prof. Plum,Lounge"
                               #create_message("accuse", cards)
                               print "Would you like to make an accusation?"
                               create_message("newSuggestion")
                           else:
                               currentCharacter.draw()
                yVal = 0
    
                ##### Checks for scratch pad #####
                for i in range(len(entries)):
                    r = entries[i].getRect()
                    if r.collidepoint(event.pos):
                        if scratchPad.scratchColorsArray[i] == True:
                            pygame.draw.line(display, RED, (r.x, r.y + 10), (r.x + 120, r.y + 10), 3)
                            scratchPad.scratchColorsArray[i] = False
                        else:
                            scratchPad.redrawEntryArea(display, r)
                            scratchPad.blitText(entries[i].getName(), r, display)
                            scratchPad.scratchColorsArray[i] = True
                    yVal += 20

                ##### Checks for making the final accusation #####
                rect = pygame.Rect(770, 460, 130, 40)
                if rect.collidepoint(event.pos):
                    print "MAKING FINAL ACCUSATION"
                    cards="Wrench,Prof. Plum,Kitchen"
                    #create_message("accuse", cards)#
                    create_message("newSuggestion")
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
