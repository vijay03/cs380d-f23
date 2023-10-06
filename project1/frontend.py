import xmlrpc.client
import xmlrpc.server
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from concurrent.futures import ThreadPoolExecutor

from collections import defaultdict
import concurrent.futures
from threading import Lock

import time
import random
import threading

baseAddr = "http://localhost:"
baseServerPort = 9000

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

class FrontendRPCServer:
    # TODO: You need to implement details for these functions.
    def __init__(self):
        self.locked_keys = dict()
        self.alive_servers  = dict()
        self.dead_servers = dict()
        self.backgroung_thread_for_heartbeat = threading.Thread(target=self.hearbeat)
        self.backgroung_thread_for_heartbeat.daemon = True
        self.backgroung_thread_for_heartbeat.start()
                
    ## put: This function routes requests from clients to proper
    ## servers that are responsible for inserting a new key-value
    ## pair or updating an existing one.
    def put(self, key, value):
        if key not in self.locked_keys:
            self.locked_keys[key] = Lock()
        self.locked_keys[key].acquire()
        with ThreadPoolExecutor(16) as executor:
            res = []
            for serverId in self.alive_servers.keys():
                res.append(executor.submit(self.alive_servers[serverId].put, key, value))
            concurrent.futures.wait(res, return_when=concurrent.futures.ALL_COMPLETED)
        self.locked_keys[key].release()

        res_result = []
        for r in res:
            res_result.append(str(r.result()))
        result = "\n".join(res_result)
        return result

    ## get: This function routes requests from clients to proper
    ## servers that are responsible for getting the value
    ## associated with the given key.
    def get(self, key):
        result = ""
        if key in self.locked_keys:
            time.sleep(0.1)
        # random_server_id = random.choice(list(self.alive_servers.keys()))
        serverId = key % len(self.alive_servers)
        return self.alive_servers[serverId].get(key)

    ## printKVPairs: This function routes requests to servers
    ## matched with the given serverIds.
    def printKVPairs(self, serverId):
        count = 0
        while count < 3:
            try:
                resp = self.alive_servers[serverId].printKVPairs()
                return resp
            except:
                resp = "Server {} is dead after retrying 3 times.".format(serverId)
                count += 1
        return resp

    ## addServer: This function registers a new server with the
    ## serverId to the cluster membership.
    def addServer(self, serverId):
        new_server = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
        server_ids = list(self.alive_servers.keys())
        if len(server_ids) != 0:
            random_server_id = random.choice(server_ids)
        
        self.alive_servers[serverId] = new_server

        # More servers exists
        if len(self.alive_servers) > 1:
            #need to copy kvs from one server to another
            try:
                kv_store = self.printKVPairs(random_server_id)
            except:
                return "Get K,V pair from " + str(random_server_id) + "failed."
            try:
                self.alive_servers[serverId].deep_copy(kv_store)
            except:
                return "Deep Copy of K,V pair to " + str(serverId) + "from" + str(random_server_id) + "failed."

        return "Success in creating new server " + str(serverId) + "K,V copied."

    ## listServer: This function prints out a list of servers that
    ## are currently active/alive inside the cluster.
    def listServer(self):
        serverList = []
        for serverId, _ in self.alive_servers.items():
            serverList.append(serverId)
        return serverList

    ## shutdownServer: This function routes the shutdown request to
    ## a server matched with the specified serverId to let the corresponding
    ## server terminate normally.
    def shutdownServer(self, serverId):
        result = self.alive_servers[serverId].shutdownServer()
        self.alive_servers.pop(serverId, None)
        return result
    
    def hearbeat(self):
        while True:
            time.sleep(1)
            dead_servers = []
            for serverId in self.alive_servers.keys():
                count = 0
                alive = False
                while count < 3:
                    try:
                        self.alive_servers[serverId].heartBeat()
                        alive = True
                        count = 3
                    except:
                        count += 1
                if not alive:
                    dead_servers.append(serverId)
        
            for id in dead_servers:
                self.alive_servers.pop(serverId)
    

server = SimpleThreadedXMLRPCServer(("localhost", 8001))
server.register_instance(FrontendRPCServer())

server.serve_forever()