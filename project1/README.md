## CS380d Project 1: Distributed Key-Value Store (KVS)

We provide guidelines to set up a basic KVS cluster configuration using
Kubernetes. For this project, we use a single local machine and simulate 
distributed environments using multiple container instances within the local
machine.

## Contents

1. `create_cluster.py`: A python script that automatically sets up Kubernetes cluster configurations.
2. `run_cluster.py`: An implementation for `event trigger`.
3. `client.py`, `frontend.py`, `server.py`: Implementations containing skeleton codes for each server instance.
4. `dockerfiles/`: dockerfiles to generate the container images of each cluster instance.
5. `yaml/`: configuration files for the Kubernetes pods of each cluster instance.

## Configure cluster

We use [Kubernetes](https://kubernetes.io/) as a cluster orchestration tool.
We will build container images for each instance pod and make Kubernetes
automatically manage them. We use [Kubespray](https://github.com/kubernetes-sigs/kubespray) to generate 
our KVS cluster orchestrated by Kubernetes over a baremetal machine.

### Tested Environment

We tested the current setup guide and implementations in the following environment only.
To prevent other potential issues, we strongly recommend that you proceed with the 
project in the same environment.

- Ubuntu18.04
- Python 3.6.9

### Download source code

```
$ cd ~/; mkdir projects; cd projects; git clone https://github.com/vijay03/cs380d-f23.git; cd cs380d-f23/project1
```

### Install dependencies

```
$ bash scripts/dependencies.sh
```

### Configure OS environment variables & SSH

There are a few environment variables that should be configured according to your own environment.

1. `$KVS_HOME`: Path to the project root directory.
2. `$USER_NAME`: Your machine's user name. The python script (`create_cluster.py`) to generate the
cluster uses this user name to access the local machine over ssh and to install required packages automatically.

```
$ export KVS_HOME=/home/cc/projects/cs380d-f23/project1
$ export USER_NAME=cc
```

Register a ssh public key as authorized key to the local machine.

```
$ ssh-keygen
```


### Install Kubernetes cluster environments

Change the ip addresses in the following file to the ip address of your local machine.
```
$ vi kubespray/inventory/kvs_cluster/inventory.ini
```
Run the following python script to install Kubernetes cluster configurations over a baremetal machine.
```
$ python3 create_cluster.py
```

Check if the cluster configurations are completed properly. The following command should show 
the list of the nodes currently managed by Kubernetes. In our case, only one node should be shown.

```
$ kubectl get nodes
NAME      STATUS   ROLES                  AGE   VERSION
master0   Ready    control-plane,master   20h   v1.22.2
```

### Build docker images
Build Docker images for cluster instance pods and upload them to your [Dockerhub](https://hub.docker.com/).
Kubernetes downloads corresponding container images from the specified docker 
repositories, when spawning cluster instances. Please change docker repository
paths to yours in pod configuration files under `yaml/pods` as well as `scrips/clean_build_docker.sh`.

```
$ bash scripts/clean_build_docker.sh
```

## Run cluster
We now run our KVS cluster. `run_cluster.py` will initialize the cluster using the
given number of clients and servers. After the initialization, it will execute an  `event trigger`
that allows you to enter and execute kvs API commands.

```
Usage: python3 run_cluster.py -c <# of clients> -s <# of servers>
$ python3 run_cluster.py -c 3 -s 2
```


