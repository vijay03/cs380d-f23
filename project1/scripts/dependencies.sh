#!/bin/bash

sudo sysctl -w net.ipv4.ip_forward=1 && sudo ufw disable && \
    sudo ln -Tfs /usr/bin/python3 /usr/bin/python

sudo apt-get update
sudo apt-get install -y python3-distutils
sudo apt-get install -y python3-pip

sudo apt remove -y ansible
sudo pip3 install -r kubespray/requirements.txt

git clone https://github.com/yaml/pyyaml.git
cd pyyaml
git checkout 5.4.1
sudo python3 setup.py install
cd ../
sudo rm -rf pyyaml

sudo pip3 install awscli cloudpickle zmq protobuf==3.19.4 boto3 kubernetes six
