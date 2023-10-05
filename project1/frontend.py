import xmlrpc.client
import xmlrpc.server
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import random
import concurrent.futures
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from collections import defaultdict

kvsServers = dict()
baseAddr = "http://localhost:"
baseServerPort = 9000
# alive_servers = dict()
# dead_servers = dict()

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

class FrontendRPCServer:
    # TODO: You need to implement details for these functions.

    ## put: This function routes requests from clients to proper
    ## servers that are responsible for inserting a new key-value
    ## pair or updating an existing one.
    # alive_servers = {}
    # dead_servers = {}
    def __init__(self):
        self.alive_servers = dict()
        self.dead_servers = dict()
        # self.multi_thread_for_get = ThreadPoolExecutor(16)
        # self.multi_thread_for_put = ThreadPoolExecutor(16)
        self.thread_for_heartbeat = threading.Thread(target=self.heartBeat)
        self.thread_for_heartbeat.daemon = True
        self.thread_for_heartbeat.start()
        

    def heartBeat(self):
        while True:
            time.sleep(1)
            for serverId in self.alive_servers.keys():
                count = 0
                alive = False
                while count < 3:
                    try:
                        alive = (self.alive_servers[serverId].heartBeat() == "OK")
                        count = 3
                    except:
                        count += 1
                if not alive:
                    self.dead_servers.put(serverId, rpcHandle)
                    self.alive_servers.pop(serverId)
        # if len(self.dead_servers) != 0:
        #     print("There are " + str(len(self.dead_servers)) + "dead servers.")
        # return "There are " + str(len(self.alive_servers)) + "alive servers." + "There are " + str(len(self.dead_servers)) + "dead servers."

    def put(self, key, value):
        for serverId, rpcHandle in self.alive_servers.items():
            rpcHandle.put(key, value)
        #print('Done')
        return 'Done-New!'
    
    def get_local(self, key):.
        random_server_id = random.choice(list(self.alive_servers.keys()))
        value = self.alive_servers[random_server_id].get(key)
        return value

    def get(self, key):
        with concurrent.futures.ThreadPoolExecutor(max_workers = 16) as executor:
            future = executor.submit(self.get_local, (key))
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                r = "[Server " + str(random_server_id) + "] Receive a get request: " + "Key = " + str(key) + " Value = " + str(result)
                return r
        

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
        #print(ans)
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
        serverList = []
        for serverId, rpcHandle in self.alive_servers.items():
            serverList.append(serverId)
        return serverList

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
