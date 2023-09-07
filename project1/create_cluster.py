import argparse
import os
import subprocess

from shared import util

def create_cluster(ssh_key):
    if 'KVS_HOME' not in os.environ:
        raise ValueError('KVS_HOME environment variable must be set to be '
                         + 'the directory where the KVS project repo is located.')

    # Organize initial cluster configurations through kubespray
    util.run_process(['./create_cluster_object.sh', ssh_key], 'scripts')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Create a KVS cluster using Kubernetes
                                    and Kubespray. If no SSH key is specified, we use the
                                    default SSH key (~/.ssh/id_rsa), and we expect that
                                    the corresponding public key has the same path and ends
                                    in .pub. If no configuration file base is specified, we
                                    use the default ($KVS_HOME/conf/kvs-base.yml).''')

    if 'KVS_HOME' not in os.environ:
        os.environ['KVS_HOME'] = "/home/" + os.environ['USER'] + "/projects/cs380d-f23/project1/"
    if 'USER_NAME' not in os.environ:
        os.environ['USER_NAME'] = os.environ['USER']

    parser.add_argument('--ssh-key', nargs='?', type=str,
                        help='The SSH key used to configure and connect to ' +
                        'each node (optional)', dest='sshkey',
                        default=os.path.join(os.environ['HOME'], '.ssh/id_rsa'))

    args = parser.parse_args()

    create_cluster(args.sshkey)
