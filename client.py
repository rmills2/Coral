from PodSixNet.Connection import ConnectionListener, connection
import Message,time
from cardAreaClass import cardArea

import sys

class ClueLessClient(ConnectionListener):
    
    
    ############## Color Declarations ##############
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    TAN= (247, 231, 160)
    
    
    ############## Create global arrays ###############
    
    images = ['study.png', 'hall.png', 'lounge.png', 'library.png', 'billiardRoom.png', 'diningRoom.png', 'conservatory.png', 'ballroom.png', 'kitchen.png']
    roomArray = ['Study','Hall','Lounge','Library','Billiard Room','Dining Room','Conservatory','Ballroom','Kitchen']
    characters = ['Player1', 'Player2', 'Player3', '4', '5']
    colorsArray = [GREEN, RED, BLUE, PURPLE, WHITE, YELLOW]
    
    x = 0
    characterArray = []
    spotArray = []
    specialRooms = []
    color = BLACK
    
    def __init__(self,host,port):
        self.gameid = None
        self.Connect((host, int(port)))
        self.card_area = None
    
    def Network(self, data):
        #print 'network data:', data
        pass
    
    def Network_hello(self,data):
        print "SERVER SAYS HELLO!"
    
    def Network_close(self, data):
        sys.exit()
    
    def Network_startgame(self, data):
        player_character = data['character']
        player_cards = data['cards']
        success,cards = Message.create_message("start")
        print "player_cards: ", player_cards
        print "start success?: ", success
        if success:
            connection.Send({"action":"success","ID":self.gameid})
        else:
            connection.Send({"action":"fail","ID":self.gameid})
    
    def Network_updateTurn(self,data):
        """ This function is to update the player's server turn index """
    
    def Network_setId(self,data):
        """ This function sets the client's ID"""
        self.gameid = data['ID']
        
    def Network_displayGameId(self,data):
        pass
    
    def Network_endgame(self,data):
        Message.create_message("end")
        sys.exit()




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
    
    clueless_client = ClueLessClient(options.host, int(options.port))
    """
    clueless_client = ClueLessClient("localhost", 8080)
    while True:
        clueless_client.Pump()
        connection.Pump()
        time.sleep(0.001)
        
