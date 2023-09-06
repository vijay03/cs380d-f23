import argparse
import random
import xmlrpc.client

clientList = dict()
baseAddr = "http://localhost:"
baseClientPort = 7000

frontend = xmlrpc.client.ServerProxy("http://localhost:8001")

clientUID = 0
serverUID = 0

if __name__ == '__main__':
    terminate = False
    while terminate != True:
        cmd = input("Enter a command: ")
        args = cmd.split(':')

        if args[0] == 'addClient':
            clientList[clientUID] = xmlrpc.client.ServerProxy(baseAddr + str(baseClientPort + clientUID))
            clientUID += 1
        elif args[0] == 'addServer':
            result = frontend.addServer(serverUID)
            serverUID += 1
            print(result)
        elif args[0] == 'listServer':
            result = frontend.listServer()
            print(result)
        elif args[0] == 'killServer':
            serverId = int(args[1])
            result = frontend.killServer(serverId)
            print(result)
        elif args[0] == 'shutdownServer':
            serverId = int(args[1])
            result = frontend.shutdownServer(serverId)
            print(result)
        elif args[0] == 'put':
            key = int(args[1])
            value = int(args[2])
            result = clientList[random.randint(1, len(clientList)) % len(clientList)].put(key, value)
            print(result)
        elif args[0] == 'get':
            key = int(args[1])
            result = clientList[random.randint(1, len(clientList)) % len(clientList)].get(key)
            print(result)
        elif args[0] == 'printKVPairs':
            serverId = int(args[1])
            result = frontend.printKVPairs(serverId)
            print(result)
        elif args[0] == 'terminate':
            terminate = True
        else:
            print("Unknown command")
