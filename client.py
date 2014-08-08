from PodSixNet.Connection import ConnectionListener, connection
import Message,time

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
        exit()
    
    def Network_yourturn(self, data):
        #torf = short for true or false
        self.turn = data["torf"]
    
    def Network_startgame(self, data):
        global ClueBoard
        print "STARTING GAME FROM CLIENT SIDE!"
        Message.create_message("start")
        connection.Send({"action":"hello","ID":self.gameid})
        import ClueBoard
        
    def Network_setId(self,data):
        
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
        
