from PodSixNet.Connection import ConnectionListener, connection
import Message,time
import jsonpickle

import sys

class ClueLessClient(ConnectionListener):
    
    def __init__(self,host,port):
        self.gameid = None
        self.Connect((host, int(port)))
        
    def Network(self, data):
        #print 'network data:', data
        pass
    
    def Network_hello(self,data):
        print "SERVER SAYS HELLO!"
    
    def Network_close(self, data):
        sys.exit()
    
    def Network_startgame(self, data):
        global ClueBoard
        player_character = data['character']
        player_cards = data['cards']
        success,cards = Message.create_message("start")
        if success:
            import ClueBoard
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
        
