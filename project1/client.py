import argparse
import xmlrpc.client
import xmlrpc.server
import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

clientId = 0
basePort = 7000

frontend = xmlrpc.client.ServerProxy("http://localhost:8001")

class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass

class ClientRPCServer:
    def put(self, key, value):
        return frontend.put(key, value)

    def get(self, key):
        return frontend.get(key)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '''To be added.''')

    parser.add_argument('-i', '--id', nargs=1, type=int, metavar='I',
                        help='Client id (required)', dest='clientId', required=True)

    args = parser.parse_args()

    clientId = args.clientId[0]

    # server = xmlrpc.server.SimpleXMLRPCServer(("localhost", basePort + clientId))
    server = AsyncXMLRPCServer(("localhost", basePort + clientId), SimpleXMLRPCRequestHandler)

    server.register_instance(ClientRPCServer())

    server.serve_forever()
