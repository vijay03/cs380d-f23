import xmlrpc.client
import xmlrpc.server
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import random

kvsServers = dict()
baseAddr = "http://localhost:"
baseServerPort = 9000

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

class FrontendRPCServer:
    # TODO: You need to implement details for these functions.

    ## put: This function routes requests from clients to proper
    ## servers that are responsible for inserting a new key-value
    ## pair or updating an existing one.
    alive_servers = {}

    def put(self, key, value):
        for server, xmlrpc_server in self.alive_servers.items():
            xmlrpc_server.put(key, value)
        print('Done')
    
    ## get: This function routes requests from clients to proper
    ## servers that are responsible for getting the value
    ## associated with the given key.
    def get(self, key):
        random_server_id = random.choice(list(self.alive_servers.keys()))
        print("Random server ID: " + random_server_id)
        print("Random server id object: " + self.alive_servers[random_server_id])
        value = self.alive_servers[random_server_id].get(key)
        print("Value read:" + value)
        # GRPC call to random server for read
        # serverId = key % len(kvsServers)
        return value

    ## printKVPairs: This function routes requests to servers
    ## matched with the given serverIds.
    def printKVPairs(self, serverId):
        '''
        Please make it printed like below (newline separated).

Key1:Val1
Key2:Val2

Key3:Val3
        '''

        ans = self.alive_servers[serverId].printKVPairs()
        print(ans)
        return ans
        #return kvsServers[serverId].printKVPairs()

    ## addServer: This function registers a new server with the
    ## serverId to the cluster membership.
    def addServer(self, serverId):
        self.alive_servers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
        return "Success"

    ## listServer: This function prints out a list of servers that
    ## are currently active/alive inside the cluster.
    def listServer(self):
        return self.alive_servers.keys()

    ## shutdownServer: This function routes the shutdown request to
    ## a server matched with the specified serverId to let the corresponding
    ## server terminate normally.
    def shutdownServer(self, serverId):
        result = self.alive_servers[serverId].shutdownServer()
        self.alive_servers.pop(serverId)
        return result

server = SimpleThreadedXMLRPCServer(("localhost", 8001))
server.register_instance(FrontendRPCServer())

server.serve_forever()
