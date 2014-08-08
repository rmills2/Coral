import PodSixNet.Channel
import PodSixNet.Server
import Message, random

from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data
    
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
    
    def Close(self):
        self._server.close(self.gameid)


class ClueLessServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.queue = ClueLessGame()
        self.currentIndex=-1
        print "STARTING UP THE SERVER"
    
    def Connected(self, channel, addr):
        self.currentIndex+=1
        print "new connection index for player: ", self.currentIndex
        channel.gameid=self.currentIndex
        channel.Send({"action":"setId","ID":self.currentIndex})
        self.queue.add_player(channel)
    
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

class ClueLessGame:
    def __init__(self):
        """
        The game logic class
        
        :param playerChannel - player channel
        :param currentIndex - current index of the player
        """
        # whose turn (1 or 0)
        self.minPlayers = 2         #  Minimum number of players to play the game
        self.active_turn = 0
        self.disprove_turn = 0
        self.playerChannels = []
    
    def add_player(self,playerChannel):
        """ This function adds another player to the game"""
        self.playerChannels.append(playerChannel)
        if len(self.playerChannels) >= self.minPlayers:
            self.startGame()
    
    def startGame(self):
        print "STARTING GAME FROM SERVER!"
        for player in self.playerChannels:
            player.Send({"action":"startgame","name":"example"})
    
    def endGame(self):
        for player in self.playerChannels:
            player.Send({"action":"endGame"})


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
