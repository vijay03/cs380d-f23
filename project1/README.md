## CS380d Project 1: Distributed Key-Value Store (KVS)

Through this project, we will learn how to build a distributed key-value store
and how to test its performance/correctness under various scenarios (such as a 
node crashing). Furthermore, we will gain some experience with the Kubernetes 
container orchestration system. This repository provides some skeleton codes
for the distributed KVS instances and guildelines to set up a basic KVS cluster 
configuration with them using Kubernetes.

## Contents

1. `create_cluster.py`: A python script that automatically sets up Kubernetes cluster configurations.
2. `run_cluster.py`: An implementation for `event trigger`.
3. `client.py`, `frontend.py`, `server.py`: Implementations containing skeleton codes for each cluster instance.
4. `dockerfiles/`: dockerfiles to generate the container images of each cluster instance.
5. `yaml/`: configuration files for the Kubernetes pods of each cluster instance.
6. `kubespray/`: A copy of [Kubespray](https://github.com/kubernetes-sigs/kubespray) repository.
7. `cluster.md`: A guildline to set up and run a KVS cluster.

## Setup & Run KVS cluster

We present a [guideline](https://github.com/vijay03/cs380d-f23/blob/master/project1/cluster.md) to set up a basic KVS cluster configuration using
Kubernetes. For this project, we use a single local machine and simulate 
distributed environments using multiple container instances within the local
machine. We provide scripts and source codes that are used to install
necessary dependencies and packages for Kubernetes cluster. You don't need to
download any third-party packages or source codes separately in addition to
what we provide through this repository. Please refer to [cluster.md](https://github.com/vijay03/cs380d-f23/blob/master/project1/cluster.md) for more details.

## Submission
Please submit a zip file containing `server.py` and `frontend.py`, and a README explaining
your design and implementation.
