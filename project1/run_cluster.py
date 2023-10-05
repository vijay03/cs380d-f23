import argparse
import os
import subprocess

import random
import xmlrpc.client

from shared import util
import concurrent.futures
baseAddr = "http://localhost:"
baseClientPort = 7000
baseFrontendPort = 8001
baseServerPort = 9000

clientUID = 0
serverUID = 0

frontend = None
clientList = dict()

def add_nodes(k8s_client, k8s_apps_client, node_type, num_nodes, prefix=None):
    global clientUID
    global serverUID

    for i in range(0, num_nodes):
        if node_type == 'server':
            server_spec = util.load_yaml('yaml/pods/server-pod.yml', prefix)
            env = server_spec['spec']['containers'][0]['env']
            util.replace_yaml_val(env, 'SERVER_ID', str(serverUID))
            server_spec['metadata']['name'] = 'server-pod-%d' % serverUID
            server_spec['metadata']['labels']['role'] = 'server-%d' % serverUID
            k8s_client.create_namespaced_pod(namespace=util.NAMESPACE, body=server_spec)
            util.check_wait_pod_status(k8s_client, 'role=server-%d' % serverUID, 'Running')
            result = frontend.addServer(serverUID)
            serverUID += 1
        elif node_type == 'client':
            client_spec = util.load_yaml('yaml/pods/client-pod.yml', prefix)
            env = client_spec['spec']['containers'][0]['env']
            util.replace_yaml_val(env, 'CLIENT_ID', str(clientUID))
            client_spec['metadata']['name'] = 'client-pod-%d' % clientUID
            client_spec['metadata']['labels']['role'] = 'client-%d' % clientUID
            k8s_client.create_namespaced_pod(namespace=util.NAMESPACE, body=client_spec)
            util.check_wait_pod_status(k8s_client, 'role=client-%d' % clientUID, 'Running')
            clientList[clientUID] = xmlrpc.client.ServerProxy(baseAddr + str(baseClientPort + clientUID))
            clientUID += 1
        else:
            print("Unknown pod type")
            exit()

def remove_node(k8s_client, k8s_apps_client, node_type, node_id):
    name = node_type + '-pod-%d' % node_id
    selector = 'role=' + node_type + '-%d' % node_id
    k8s_client.delete_namespaced_pod(name, namespace=util.NAMESPACE)
    util.check_wait_pod_status(k8s_client, selector, 'Terminating')

def addClient(k8s_client, k8s_apps_client, prefix):
    add_nodes(k8s_client, k8s_apps_client, 'client', 1, prefix)

def addServer(k8s_client, k8s_apps_client, prefix):
    add_nodes(k8s_client, k8s_apps_client, 'server', 1, prefix)

def listServer():
    result = frontend.listServer()
    print(result)

def killServer(k8s_client, k8s_apps_client, serverId):
    remove_node(k8s_client, k8s_apps_client, 'server', serverId)

def shutdownServer(k8s_client, k8s_apps_client, serverId):
    result = frontend.shutdownServer(serverId)
    remove_node(k8s_client, k8s_apps_client, 'server', serverId)
    print(result)

def put(key, value):
    result = clientList[random.randint(1, 100000) % len(clientList)].put(key, value)
    print(result)

def get(key):
    print('Request for key: {key}')
    result = clientList[random.randint(1, len(clientList)) % len(clientList)].get(key)
    print('Request for key later: {key}')
    print(result)

def printKVPairs(serverId):
    result = frontend.printKVPairs(serverId)
    print(result)

def init_cluster(k8s_client, k8s_apps_client, num_client, num_server, ssh_key, prefix):
    global frontend

    print('Creating a frontend pod...')
    frontend_spec = util.load_yaml('yaml/pods/frontend-pod.yml', prefix)
    env = frontend_spec['spec']['containers'][0]['env']
    k8s_client.create_namespaced_pod(namespace=util.NAMESPACE, body=frontend_spec)
    util.check_wait_pod_status(k8s_client, 'role=frontend', 'Running')
    frontend = xmlrpc.client.ServerProxy(baseAddr + str(baseFrontendPort))

    print('Creating server pods...')
    add_nodes(k8s_client, k8s_apps_client, 'server', num_server, prefix)

    print('Creating client pods...')
    add_nodes(k8s_client, k8s_apps_client, 'client', num_client, prefix)

def event_trigger(k8s_client, k8s_apps_client, prefix):
    terminate = False
    while terminate != True:
        cmd = input("Enter a command: ")
        args = cmd.split(':')
        print(str(args))

        if args[0] == 'addClient':
            addClient(k8s_client, k8s_apps_client, prefix)
        elif args[0] == 'addServer':
            addServer(k8s_client, k8s_apps_client, prefix)
        elif args[0] == 'listServer':
            listServer()
        elif args[0] == 'killServer':
            serverId = int(args[1])
            killServer(k8s_client, k8s_apps_client, serverId)
        elif args[0] == 'shutdownServer':
            serverId = int(args[1])
            shutdownServer(k8s_client, k8s_apps_client, serverId)
        elif args[0] == 'put':
            key = int(args[1])
            value = int(args[2])
            put(key, value)
        elif args[0] == 'get':
            keys = []
            for i in range(len(args)):
                if(args[i] == 'get'):
                    key = int(args[i + 1])
                    keys.append(key)
            # key = int(args[1])
            print(str(keys))
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Submit GET requests for each key concurrently
                    print("Inside")
                    results = list(executor.map(get, keys))
                    # for future in concurrent.futures.as_completed(results):
                    #     print(results)
                    print("Done res")
            except Exception as e:
                print("In error")
                print(str(e))
            # get(key)
        elif args[0] == 'printKVPairs':
            serverId = int(args[1])
            printKVPairs(serverId)
        elif args[0] == 'terminate':
            terminate = True
        else:
            print("Unknown command")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Create a KVS cluster using Kubernetes
                                    and Kubespray. If no SSH key is specified, we use the
                                    default SSH key (~/.ssh/id_rsa), and we expect that
                                    the corresponding public key has the same path and ends
                                    in .pub. If no configuration file base is specified, we
                                    use the default ($KVS_HOME/conf/kvs-base.yml).''')

    if 'KVS_HOME' not in os.environ:
        os.environ['KVS_HOME'] = "/home/" + os.environ['USER'] + "/projects/cs380d-f23/project1/"

    parser.add_argument('-c', '--client', nargs=1, type=int, metavar='C',
                        help='The number of client nodes to start with ' +
                        '(required)', dest='client', required=True)
    parser.add_argument('-s', '--server', nargs=1, type=int, metavar='S',
                        help='The number of server nodes to start with ' +
                        '(required)', dest='server', required=True)
    parser.add_argument('--ssh-key', nargs='?', type=str,
                        help='The SSH key used to configure and connect to ' +
                        'each node (optional)', dest='sshkey',
                        default=os.path.join(os.environ['HOME'], '.ssh/id_rsa'))

    args = parser.parse_args()

    prefix = os.environ['KVS_HOME']

    k8s_client, k8s_apps_client = util.init_k8s()

    init_cluster(k8s_client, k8s_apps_client, args.client[0], args.server[0], args.sshkey, prefix)

    event_trigger(k8s_client, k8s_apps_client, prefix)
