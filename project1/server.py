import argparse
import xmlrpc.client
import xmlrpc.server

serverId = 0
basePort = 9000

class KVSRPCServer:
    def put(self, key, value):
        return "[Server " + str(serverId) + "] Receive a put request: " + "Key = " + str(key) + ", Val = " + str(value)

    def get(self, key):
        return "[Server " + str(serverId) + "] Receive a get request: " + "Key = " + str(key)

    def printKVPairs(self):
        return "[Server " + str(serverId) + "] Receive a request printing all KV pairs stored in this server"

    def shutdownServer(self):
        return "[Server " + str(serverId) + "] Receive a request for a normal shutdown"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '''To be added.''')

    parser.add_argument('-i', '--id', nargs=1, type=int, metavar='I',
                        help='Server id (required)', dest='serverId', required=True)

    args = parser.parse_args()

    serverId = args.serverId[0]

    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", basePort + serverId))
    server.register_instance(KVSRPCServer())

    server.serve_forever()
