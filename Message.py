import pygame, sys, time, multiprocessing
from pygame.locals import *
from CardDeck import CardDeck, Card
from forms import Form, Select, Button,Text
import subprocess, os

pygame.font.init()
PYGBUTTON_FONT = pygame.font.Font('freesansbold.ttf', 14)

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)

class MessageButton(object):
    def __init__(self, rect=None, caption='', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None, normal=None, down=None, highlight=None):
        """Create a new button object. Parameters:
            rect - The size and position of the button as a pygame.Rect object
                or 4-tuple of integers.
            caption - The text on the button (default is blank)
            bgcolor - The background color of the button (default is a light
                gray color)
            fgcolor - The foreground color (i.e. the color of the text).
                Default is black.
            font - The pygame.font.Font object for the font of the text.
                Default is freesansbold in point 14.
            normal - A pygame.Surface object for the button's normal
                appearance.
            down - A pygame.Surface object for the button's pushed down
                appearance.
            highlight - A pygame.Surface object for the button's appearance
                when the mouse is over it.

            If the Surface objects are used, then the caption, bgcolor,
            fgcolor, and font parameters are ignored (and vice versa).
            Specifying the Surface objects lets the user use a custom image
            for the button.
            The normal, down, and highlight Surface objects must all be the
            same size as each other. Only the normal Surface object needs to
            be specified. The others, if left out, will default to the normal
            surface.
            """
        if rect is None:
            self._rect = pygame.Rect(0, 0, 30, 60)
        else:
            self._rect = pygame.Rect(rect)

        self._caption = caption
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor

        if font is None:
            self._font = PYGBUTTON_FONT
        else:
            self._font = font

        # tracks the state of the button
        self.buttonDown = False # is the button currently pushed down?
        self.mouseOverButton = False # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False # was the last mouse down event over the mouse button? (Used to track clicks.)
        self._visible = True # is the button visible
        self.customSurfaces = False # button starts as a text button instead of having custom images for each surface

        if normal is None:
            # create the surfaces for a text button
            self.surfaceNormal = pygame.Surface(self._rect.size)
            self.surfaceDown = pygame.Surface(self._rect.size)
            self.surfaceHighlight = pygame.Surface(self._rect.size)
            self._update() # draw the initial button images
        else:
            # create the surfaces for a custom image button
            self.setSurfaces(normal, down, highlight)
    
    def get_caption_name(self):
        return self._caption
    
    def handleEvent(self, eventObj):
        """All MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN event objects
        created by Pygame should be passed to this method. handleEvent() will
        detect if the event is relevant to this button and change its state.

        There are two ways that your code can respond to button-events. One is
        to inherit the MessageButton class and override the mouse*() methods. The
        other is to have the caller of handleEvent() check the return value
        for the strings 'enter', 'move', 'down', 'up', 'click', or 'exit'.

        Note that mouseEnter() is always called before mouseMove(), and
        mouseMove() is always called before mouseExit(). Also, mouseUp() is
        always called before mouseClick().

        buttonDown is always True when mouseDown() is called, and always False
        when mouseUp() or mouseClick() is called. lastMouseDownOverButton is
        always False when mouseUp() or mouseClick() is called."""

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return []

        retVal = []

        hasExited = False
        if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
            # if mouse has entered the button:
            self.mouseOverButton = True
            self.mouseEnter(eventObj)
            retVal.append('enter')
        elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
            # if mouse has exited the button:
            self.mouseOverButton = False
            hasExited = True # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

        if self._rect.collidepoint(eventObj.pos):
            # if mouse event happened over the button:
            if eventObj.type == MOUSEMOTION:
                self.mouseMove(eventObj)
                retVal.append('move')
            elif eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouseDown(eventObj)
                retVal.append('down')
        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        doMouseClick = False
        if eventObj.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouseUp(eventObj)
                retVal.append('up')

            if doMouseClick:
                self.buttonDown = False
                self.mouseClick(eventObj)
                retVal.append('click')

        if hasExited:
            self.mouseExit(eventObj)
            retVal.append('exit')

        return retVal

    def draw(self, surfaceObj):
        """Blit the current button's appearance to the surface object."""
        if self._visible:
            if self.buttonDown:
                surfaceObj.blit(self.surfaceDown, self._rect)
            elif self.mouseOverButton:
                surfaceObj.blit(self.surfaceHighlight, self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal, self._rect)

    
    def _update(self):
        """Redraw the button's Surface object. Call this method when the button has changed appearance."""
        if self.customSurfaces:
            self.surfaceNormal    = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
            self.surfaceDown      = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
            self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
            return

        w = self._rect.width # syntactic sugar
        h = self._rect.height # syntactic sugar

        # fill background color for all buttons
        self.surfaceNormal.fill(self.bgcolor)
        self.surfaceDown.fill(self.bgcolor)
        self.surfaceHighlight.fill(self.bgcolor)

        # draw caption text for all buttons
        captionSurf = self._font.render(self._caption, True, self.fgcolor, self.bgcolor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)

        # draw border for normal button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self.surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        self.surfaceHighlight = self.surfaceNormal


    def mouseClick(self, event):
        pass # This class is meant to be overridden.
    def mouseEnter(self, event):
        pass # This class is meant to be overridden.
    def mouseMove(self, event):
        pass # This class is meant to be overridden.
    def mouseExit(self, event):
        pass # This class is meant to be overridden.
    def mouseDown(self, event):
        pass # This class is meant to be overridden.
    def mouseUp(self, event):
        pass # This class is meant to be overridden.


    def setSurfaces(self, normalSurface, downSurface=None, highlightSurface=None):
        """Switch the button to a custom image type of button (rather than a
        text button). You can specify either a pygame.Surface object or a
        string of a filename to load for each of the three button appearance
        states."""
        if downSurface is None:
            downSurface = normalSurface
        if highlightSurface is None:
            highlightSurface = normalSurface

        if type(normalSurface) == str:
            self.origSurfaceNormal = pygame.image.load(normalSurface)
        if type(downSurface) == str:
            self.origSurfaceDown = pygame.image.load(downSurface)
        if type(highlightSurface) == str:
            self.origSurfaceHighlight = pygame.image.load(highlightSurface)

        if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() != self.origSurfaceHighlight.get_size():
            raise Exception('foo')

        self.surfaceNormal = self.origSurfaceNormal
        self.surfaceDown = self.origSurfaceDown
        self.surfaceHighlight = self.origSurfaceHighlight
        self.customSurfaces = True
        self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))



    def _propGetCaption(self):
        return self._caption


    def _propSetCaption(self, captionText):
        self.customSurfaces = False
        self._caption = captionText
        self._update()


    def _propGetRect(self):
        return self._rect


    def _propSetRect(self, newRect):
        # Note that changing the attributes of the Rect won't update the button. You have to re-assign the rect member.
        self._update()
        self._rect = newRect


    def _propGetVisible(self):
        return self._visible


    def _propSetVisible(self, setting):
        self._visible = setting


    def _propGetFgColor(self):
        return self._fgcolor


    def _propSetFgColor(self, setting):
        self.customSurfaces = False
        self._fgcolor = setting
        self._update()


    def _propGetBgColor(self):
        return self._bgcolor


    def _propSetBgColor(self, setting):
        self.customSurfaces = False
        self._bgcolor = setting
        self._update()


    def _propGetFont(self):
        return self._font


    def _propSetFont(self, setting):
        self.customSurfaces = False
        self._font = setting
        self._update()


    caption = property(_propGetCaption, _propSetCaption)
    rect = property(_propGetRect, _propSetRect)
    visible = property(_propGetVisible, _propSetVisible)
    fgcolor = property(_propGetFgColor, _propSetFgColor)
    bgcolor = property(_propGetBgColor, _propSetBgColor)
    font = property(_propGetFont, _propSetFont)

class Message:
    
    START_MESSAGE = "Welcome, the game has started"
    WIN_MESSAGE = "Congratulations, you have won the game!"
    LOSE_MESSAGE = "Sorry, you have lost the game."
    INVALID_MOVE = "Invalid Move. Please select another area."
    END_GAME =  "Sorry, a player has left the game."
    MOVE_MESSAGE = "It is your turn. Please make a move."
    SUGGESTION = "A suggestion was made:"
    DISPROVE = "Your suggestion was disproved:"
    INCOMPLETE = "Please select a card to disprove the suggestion."
    MUSTDISPROVE = "It is your turn to disprove the suggestion."
    CUSTOM = "Hello, how are you doing?"
    
    MESSAGE_STRINGS = {
                      "Invalid Move":INVALID_MOVE,
                      "End Game":END_GAME,
                      "Start Game": START_MESSAGE,
                      "Player Win": WIN_MESSAGE,
                      "Player Lose":LOSE_MESSAGE,
                      "Player Move":MOVE_MESSAGE,
                      "Suggestion":SUGGESTION,
                      "Disprove": DISPROVE,
                      "Must Disprove": MUSTDISPROVE,
                      "Incomplete":INCOMPLETE,
                      "Custom":CUSTOM,
                      }
    MESSAGE_LOCATION = {
                        "Invalid Move":(70,50),
                      "End Game": (120,50),
                      "Start Game": (120,50),
                      "Player Win": (80,50),
                      "Player Lose":(140,50),
                      "Player Move":(100,50),
                      "Suggestion":(160,20),
                      "Disprove":(130,20),
                      "Must Disprove": (80,60),
                      "Incomplete":(30,50),
                      "Custom":(140,50)
                        }
    
    SUGGESTION_TYPE_LOCATION = {"character":(230,55),"weapon":(230,85),"room":(230,115)}
    
    background_color = (255,255,255)
    window_width, window_height = (600, 200)
    message_font = pygame.font.SysFont('Arial', 25)
    accusation_font = pygame.font.SysFont('Arial', 20)
    
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        pygame.init()
    
    def get_accusation(self,card,cardtype):
        if card == None:
            return ""
        name = card.get_name()
        if cardtype == "weapon":
            return "with a {0}".format(name)
        elif cardtype == "room":
            return "in the {0}".format(name)
        elif cardtype == "character":
            return name
        else:
            return 'UNKNOWN CARDTYPE'
    
    def get_accusation_position(self,card,cardtype):
        return self.SUGGESTION_TYPE_LOCATION[cardtype]
    
    def getScreen(self,message_type,accusationPage=False):
        """ """
        if accusationPage:
            screen = pygame.display.set_mode((self.window_width/2, self.window_height*3.5))
        else:
            screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(message_type)
        screen.fill(self.background_color)
        pygame.display.flip()
        return screen
    
    def showAccusationScreen(self,message_type,buttons,messages):
        """ This function shows the message screen
        
        :param message_type - type string -- message type to display. Must be a key from the MESSAGE_STRINGS
        :param buttons - type list - list of MessageButtons to draw
        :param message - type list - list of messages to render (type Surface)
        
        """
        screen = self.getScreen(message_type)
        
        running = True
        form_input = None
        success = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    success = False
                    running = False
                for x in xrange(len(buttons)):
                    button = buttons[x]
                    eventhandler = button.handleEvent(event)
                    if 'exit' in eventhandler:
                        success = False
                        running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "disprove":
                        form_input = self.disproveAccusation(message_type,messages)
                        if form_input == None:
                            self.showNonAccusationScreen("Incomplete")
                        else:
                            running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "skip":
                        running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "ok":
                        running = False
            screen.fill(self.background_color)
            for message_obj in messages:
                message = message_obj[0]
                message_position = message_obj[1]
                message_str = message_obj[2]
                #screen.blit(self.message_font.render(self.MESSAGE_STRINGS[message_type],True,BLACK),message_position)
                screen.blit(message,message_position)
            for button in buttons:
                button.draw(screen)
            pygame.display.update()
        return success, form_input
    
    def disproveAccusation(self,message_type,accusation_lines):
        card_deck = CardDeck()
        
        screen = self.getScreen(message_type,True)
        
        accusation_form = Form(False)
        accusation_form.add_object('title', Text('Accusation:', label_style=['bold']))
        for k in xrange(len(accusation_lines)):
            print "accusation_lines: ", accusation_lines[k]
            accusation_message, accusation_pos,accusation_message_str = accusation_lines[k]
            accusation_form.add_object('accusation_{0}'.format(k), Text('{0}'.format(accusation_message_str), label_style=['bold']))
        
        accusation_form.add_object('disprove_title', Text('Select card(s) to disprove:', label_style=['bold','underline']))
        character_menu = Select(border_width=2, top=50)
        character_list = card_deck.get_cardlist("character")
        for character_name in character_list:
            character_menu.add_option(character_name,character_name)
        accusation_form.add_object('character', character_menu)
        
        accusation_form.add_object('weapon_title', Text('with a', label_style=['bold']))
        
        weapon_list = card_deck.get_cardlist("weapon")
        weapon_menu = Select(border_width=2, top=50)
        for weapon_name in weapon_list:
            weapon_menu.add_option(weapon_name,weapon_name)
        accusation_form.add_object('weapon', weapon_menu)
        
        accusation_form.add_object('room_title', Text('in the', label_style=['bold']))
        
        room_list = card_deck.get_cardlist("room")
        room_menu = Select(border_width=2, top=50)
        for room_name in room_list:
            room_menu.add_option(room_name,room_name)
        accusation_form.add_object('room', room_menu)
        
        accusation_form.add_object('submit', Button('Disprove', accusation_form.submit, ()))
        accusation_form.add_object('skip', Button('Skip', accusation_form.skip, ()))
        
        form_input = accusation_form.run(screen)
        
        if accusation_form._skip:
            return {}
        elif len(form_input) == 0:
            return None
        
        return form_input
    
    def get_accusationText(self,message_type="Suggestion",character_card=None,weapon_card=None,room_card=None):
        
        message_position = self.get_message_position(message_type)
        message_string = self.message_font.render(self.MESSAGE_STRINGS[message_type],True,BLACK)
        messages = [(message_string,message_position,"")]
        
        card_order = [character_card,weapon_card,room_card]
        card_types = ["character","weapon","room"]
        for x in xrange(len(card_order)):
            card = card_order[x]
            cardtype = card_types[x]
            accusation_str = self.get_accusation(card,cardtype)
            message_str = self.accusation_font.render(accusation_str,True,BLACK)
            message_pos = self.get_accusation_position(card,cardtype)
            messages.append((message_str,message_pos,accusation_str))
        
        print "FINAL MESSAGES: ", messages
        return messages
    
    def showAccusation(self,message_type,character_card=None,weapon_card=None,room_card=None,mustDisprove=False):
        """ This function notifies all players of the accusation"""
        
        if not mustDisprove:
            buttons = [MessageButton((270,150, 60, 30), "OK")]
        else:
            buttons = [MessageButton((200,150, 80, 30), "Disprove"),MessageButton((300,150, 80, 30), "Skip")]
        
        messages = self.get_accusationText(message_type,character_card,weapon_card,room_card)
        
        return self.showAccusationScreen(message_type,buttons,messages)
    
    def showError(self,errortype):
        """ This function shows the user the error"""
        pass
    
    def startGame(self):
        """ This function tells the user that the game has begun"""
        message_type = "Start Game"
        return self.showNonAccusationScreen(message_type)
        
    
    def get_message_position(self,message_type):
        return self.MESSAGE_LOCATION[message_type]
    
    def showNonAccusationScreen(self,message_type,character_card=None,weapon_card=None,room_card=None):
        if all([character_card,weapon_card,room_card]):
            buttons = [MessageButton((200,150, 80, 30), "Disprove"),MessageButton((300,150, 80, 30), "Skip")]
        else:
            buttons = [MessageButton((270,120, 60, 30), "OK")]
        
        message_position = self.get_message_position(message_type)
        message_string = self.message_font.render(self.MESSAGE_STRINGS[message_type],True,BLACK)
        
        return self.showScreen(message_type,buttons,[(message_string,message_position)],character_card,weapon_card,room_card)
    
    def showScreen(self,message_type,buttons,messages,character_card=None,weapon_card=None,room_card=None):
        """ This function shows the message screen
        
        :param message_type - type string -- message type to display. Must be a key from the MESSAGE_STRINGS
        :param buttons - type list - list of MessageButtons to draw
        :param message - type list - list of messages to render (type Surface)
        
        """
        screen = self.getScreen(message_type)
        
        form_input = None
        running = True
        success = True
        while running:
            
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    success = False
                    running = False
                for x in xrange(len(buttons)):
                    button = buttons[x]
                    eventhandler = button.handleEvent(event)
                    if 'exit' in eventhandler:
                        success = False
                        running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "disprove":
                        accusation_message = self.get_accusationText("Suggestion",character_card,weapon_card,room_card)
                        form_input = self.disproveAccusation(message_type,accusation_message)
                        if form_input == None:
                            self.showNonAccusationScreen("Incomplete")
                        else:
                            running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "good":
                        running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "terrible":
                        running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "skip":
                        running = False
                    elif 'click' in eventhandler and button.get_caption_name().lower() == "ok":
                        running = False
                    
            screen.fill(self.background_color)
            for message,message_position in messages:
                #screen.blit(self.message_font.render(self.MESSAGE_STRINGS[message_type],True,BLACK),message_position)
                screen.blit(message,message_position)
            for button in buttons:
                button.draw(screen)
            
            pygame.display.update()
        return success, form_input
    
    def showCustomScreen(self,message_type):
        
        buttons = [MessageButton((200,150, 80, 30), "Good"),MessageButton((300,150, 80, 30), "Terrible")]
        
        message_position = self.get_message_position(message_type)
        message_string = self.message_font.render(self.MESSAGE_STRINGS[message_type],True,BLACK)
        
        return self.showScreen(message_type,buttons,[(message_string,message_position)])
    
    def showWin(self):
        message_type = "Player Win"
        return self.showNonAccusationScreen(message_type)
    
    def showLose(self):
        message_type = "Player Lose"
        return self.showNonAccusationScreen(message_type)
    
    def showEnd(self):
        """ This function tells the user has ended because of a player disruption"""
        message_type = "End Game"
        return self.showNonAccusationScreen(message_type)
    
    def showInvalidMove(self):
        message_type = "Invalid Move"
        return self.showNonAccusationScreen(message_type)
    
    def showMove(self):
        message_type = "Player Move"
        return self.showNonAccusationScreen(message_type)
    
    def mustDisproveTurn(self,character_card,weapon_card,room_card):
        message_type = "Must Disprove"
        
        return self.showNonAccusationScreen(message_type,character_card,weapon_card,room_card)
    
    def showDisprove(self,character_card,weapon_card,room_card):
        message_type = "Disprove"
        return self.showAccusation(message_type,character_card,weapon_card,room_card)
    
    def custom(self):
        message_type = "Custom"
        return self.showCustomScreen(message_type)
    
def execute_accusation(message,options):
    global parser
    
    if not options.cards:
        parser.error("Must specify cards for accusation")
        return
    
    char_card, weapon_card, room_card = get_accusationCards(options)
    
    if not all([char_card,weapon_card,room_card]):
        parser.error("Character card, weapon card, and/or room card must be specified")
        return
    
    return message.showAccusation("Suggestion",char_card,weapon_card,room_card)

def execute_mustDisprove(message,options):
    global parser
    
    if not options.cards:
        parser.error("Must specify cards for accusation")
        return
    
    char_card, weapon_card, room_card = get_accusationCards(options)
    
    if not all([char_card,weapon_card,room_card]):
        parser.error("Character card, weapon card, and/or room card must be specified")
        return
    
    return message.mustDisproveTurn(char_card,weapon_card,room_card)


def get_accusationCards(options):
    """ This function parses the cards from the options and returns Card objects"""
    card_deck = CardDeck()
    char_card = None
    weapon_card = None
    room_card = None
    card_names = options.cards.split(",")
    for card_name in card_names:
        requested_card = card_deck.get_card(card_name)
        cardtype = requested_card.get_cardtype()
        if cardtype == "character":
            char_card = requested_card
        elif cardtype == "weapon":
            weapon_card = requested_card
        elif cardtype == "room":
            room_card = requested_card
    return char_card, weapon_card, room_card

def execute_disprove(message,options):
    global parser
    
    if not options.cards:
        parser.error("Must specify cards for accusation")
        return None, None
    
    char_card, weapon_card, room_card = get_accusationCards(options)
    
    if not any([char_card,weapon_card,room_card]):
        parser.error("Character card, weapon card, or room card must be specified")
        return None, None
    
    return message.showDisprove(char_card,weapon_card,room_card)

def test():
    card_deck = CardDeck()
    
    message_types = ['start', 'move', 'invalidMove', 'accuse','mustDisprove', 'disprove', 'win', 'lose', 'end']
    for message_type in message_types:
        if message_type != "accuse" and message_type != "disprove" and message_type != "mustDisprove":
            create_message(message_type)
        else:
            char_card = None
            weapon_card = None
            room_card = None
            need_card_types = ['character','weapon','room']
            for cardtype in need_card_types:
                requested_card = card_deck.get_random_card(cardtype)
                if requested_card != None:
                    if cardtype == "character":
                        char_card = requested_card
                    elif cardtype == "weapon":
                        weapon_card = requested_card
                    elif cardtype == "room":
                        room_card = requested_card
            card_names = ",".join([x.get_name() for x in [char_card,weapon_card,room_card]])
            create_message(message_type,card_names)

def execute(options):
    
    message = Message()
    if options.start:
        print message.startGame()
    elif options.move:
        print message.showMove()
    elif options.invalid_move:
        print message.showInvalidMove()
    elif options.accuse:
        print execute_accusation(message,options)
    elif options.mustDisprove:
        print execute_mustDisprove(message,options)
    elif options.disprove:
        print execute_disprove(message,options)
    elif options.win:
        print message.showWin()
    elif options.lose:
        print message.showLose()
    elif options.end:
        print message.showEnd()
    elif options.test:
        print test()
    elif options.custom:
        print message.custom()
    else:
        parser.error("No options specified")


def create_message(message_type,cards=None):
    """ This function creates a separate process to show the message
    
    :param message_type - type str -- message type
    :param cards - type str -- comma-separated name of cards
     """
    commands = ["python",os.path.abspath(__file__)]
    
    if message_type == "start":
        commands.append("--start")
    elif message_type == "move":
        commands.append("--move")
    elif message_type == "invalidMove":
        commands.append("--invalidMove")
    elif message_type == "accuse":
        commands.extend(["--accuse","--cards","'{0}'".format(cards)])
    elif message_type =="mustDisprove":
        commands.extend(["--mustDisprove","--cards","'{0}'".format(cards)])
    elif message_type == "disprove":
        commands.extend(["--disprove","--cards","'{0}'".format(cards)])
    elif message_type == "win":
        commands.append("--win")
    elif message_type == "lose":
        commands.append("--lose")
    elif message_type == "end":
        commands.append("--end")
    elif message_type == "custom":
        commands.append("--custom")
    else:
        print >> sys.stderr, "ERROR: UNKNOWN MESSAGE TYPE: ", message_type
    
    commands.extend(['2>','/dev/null'])
    execute = os.popen(" ".join(commands),'r')
    result = eval(execute.read())
    execute.close()
    return result

if __name__ == "__main__":
    import optparse
    
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option("--start",
                      action="store_true", dest="start", default=False,
                      help="Show start message")
    
    parser.add_option("--move",
                      action="store_true", dest="move", default=False,
                      help="Show move message")
    
    parser.add_option("--invalidMove",
                      action="store_true", dest="invalid_move", default=False,
                      help="Show invalid move message")
    
    parser.add_option("--accuse",
                      action="store_true", dest="accuse", default=False,
                      help="Show accuse message")
    
    parser.add_option("--mustDisprove",
                      action="store_true", dest="mustDisprove", default=False,
                      help="Show Must Disprove message")
    
    parser.add_option("--disprove",
                      action="store_true", dest="disprove", default=False,
                      help="Show accuse message")
    
    parser.add_option("--win",
                      action="store_true", dest="win", default=False,
                      help="Show win message")
    
    parser.add_option("--lose",
                      action="store_true", dest="lose", default=False,
                      help="Show lose message")
    
    parser.add_option("--end",
                      action="store_true", dest="end", default=False,
                      help="Show end message")
    
    parser.add_option("--cards", dest="cards", default=False,
                      help="List of cards (comma separated)")
    
    parser.add_option("--test",
                      action="store_true", dest="test", default=False,
                      help="Run tests")
    
    parser.add_option("--custom",
                      action="store_true", dest="custom", default=False,
                      help="Custom message")
    
    (options, args) = parser.parse_args()
    
    execute(options)
    