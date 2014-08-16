import PodSixNet.Channel
import PodSixNet.Server
import Message, random
from CardDeck import CardDeck
import jsonpickle, sys
import random

from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        #print data
        pass
    
    def Network_place(self, data):
        #deconsolidate all of the data from the dictionary
     
        #horizontal or vertical?
        hv = data["is_horizontal"]
        #x of placed line
        x = data["x"]
     
        #y of placed line
        y = data["y"]
     
        #player number (1 or 0)
        num=data["num"]
     
        #id of game given by server at start of game
        self.gameid = data["gameid"]
     
        #tells server to place line
        self._server.placeLine(hv, x, y, data, self.gameid, num)
    
    def Network_testaction(self,data):
        Message.create_message("start")
    
    def Network_hello(self,data):
        print "CLIENT {0} SAYS HELLO TO YOU, SERVER!".format(data['ID'])
    
    def Network_success(self,data):
        print "CLIENT {0} RESPONSES WITH SUCCESS!".format(data['ID'])
    
    def Network_fail(self,data):
        print "CLIENT {0} RESPONSES WITH FAILURE!".format(data['ID'])
    
    def Network_playerMove(self,data):
        print "Updating PlayerMove from ClientChannel!"
        spotArrayIndex = data['spotArrayIndex']
        playerId = data['playerId']
        self._server.update_playerMove(spotArrayIndex,playerId)
    
    def Network_newSuggestion(self,data):
        self._server.make_suggestion(data)
    
    def Close(self):
        self._server.close(self.gameid)

class ClueLessGame:
    def __init__(self):
        """
        The game logic class
        
        :param playerChannel - player channel
        :param currentIndex - current index of the player
        """
        
    
    
        
class ClueLessServer(PodSixNet.Server.Server,ClueLessGame):
 
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.currentIndex=-1
        print "STARTING UP THE SERVER"
        
        self.card_deck = CardDeck()
        
        self.confidential_card_types = ['character','weapon','room']
        self.confidential_file = []
        
        self.minPlayers = 3         #  Minimum number of players to play the game
        self.active_turn = 0
        self.disprove_turn = 0
        self.playerChannels = []
        
        self.select_confidential_cards()
    
    def make_suggestion(self,data):
        """ Notify all users of all the suggestion """
        cards = data['cards']
        playerId = data['playerId']
        
        self.broadcast_suggestion(cards,playerId)
    
    def broadcast_suggestion(self,cards,playerId):
        for x in xrange(len(self.playerChannels)):
            if x == playerId: continue
            
            player = self.playerChannels[x]
            player.Send({"action":"newSuggestion","cards":cards})
    
    def Connected(self, channel, addr):
        self.currentIndex+=1
        print "new connection index for player: ", self.currentIndex
        channel.gameid=self.currentIndex
        channel.Send({"action":"setId","ID":self.currentIndex})
        self.add_player(channel)
    
    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid==gameid][0]
            game.player0.Send({"action":"close"})
            game.player1.Send({"action":"close"})
        except:
            pass
    def tick(self):
        # Check for any wins
        # Loop through all of the squares
        self.Pump()
    
    def select_confidential_cards(self):
        """ This function selects cards from the confidential file"""
        for cardtype in self.confidential_card_types:
            self.confidential_file.append(self.card_deck.get_random_card(cardtype))
    
    def add_player(self,playerChannel):
        """ This function adds another player to the game"""
        self.playerChannels.append(playerChannel)
        if len(self.playerChannels) >= self.minPlayers:
            self.startGame()
    
    def startGame(self):
        print "STARTING GAME FROM SERVER!"
        
        assigned_characters,assigned_cards = self.distribute_cards()
        self.active_turn = random.choice(xrange(len(self.playerChannels)))
        for x in xrange(len(self.playerChannels)):
            player = self.playerChannels[x]
            player_character = assigned_characters[x].get_name()
            player_cards = [card.get_name() for card in assigned_cards[x]]
            player.Send({"action":"startgame","youAre":x,"turn":self.active_turn,"character":player_character,"cards":player_cards,'numplayers':len(self.playerChannels)})
    
    def distribute_cards(self):
        """ This function iterates through the card deck, randomly assigns players a character, and the rest of cards in the deck """
        card_tracker = self.confidential_file
        assigned_chars = []     # Assigned character for each player
        assigned_cards = [[] for x in xrange(len(self.playerChannels))]    # Assigned cards for each player
        for x in xrange(len(self.playerChannels)):
            player = self.playerChannels[x]
            char_card = self.card_deck.get_random_card("character",card_tracker)
            
            card_tracker.append(char_card)
            assigned_chars.append(char_card)
        
        x = 0
        while len(card_tracker) < self.card_deck.length():
            
            card = self.card_deck.get_random_card(None,card_tracker)
            x = x+1 if x < len(assigned_cards)-1 else 0
            assigned_cards[x].append(card)
            card_tracker.append(card)
        
        print "final assigned_chars: ", assigned_chars
        print "final assigned_cards: ", assigned_cards
        
        return assigned_chars,assigned_cards
    
    
    def increment_active_turn(self):
        self.active_turn = self.active_turn+1 if self.active_turn < len(self.playerChannels)-1 else 0
    
    def updateTurn(self):
        self.increment_active_turn()
        
        for x in xrange(len(self.playerChannels)):
            player = self.playerChannels[x]
            player.Send({"action":"updateTurn","turn":self.active_turn})
    
    def endGame(self):
        for player in self.playerChannels:
            player.Send({"action":"endGame"})
    
    def update_playerMove(self,spotArrayIndex,playerId):
        
        for x in xrange(len(self.playerChannels)):
            if x == playerId: continue  # skip the previous active players update
            
            player = self.playerChannels[x]
            player.Send({"action":"movePlayer","spotArrayIndex":spotArrayIndex})
        
        self.updateTurn()


if __name__ == "__main__":
    import optparse
    """
    usage = "usage: %prog [options]"
    
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--host", dest="host", help="address to run server on")
    
    parser.add_option('-p',"--port",dest="port",
                      help="Port to run server on ")
    
    (options, args) = parser.parse_args()
    if not options.host:
        parser.error("Must specify host to run server on")
    
    if not options.port:
        parser.error("Must specify port to run server on")
    
    clueless_server = ClueLessServer(localaddr=(options.host, int(options.port)))
    """
    clueless_server = ClueLessServer(localaddr=("localhost", 8080))
    
    while True:
        clueless_server.tick()
        sleep(0.01)
