#!/bin/bash

sysctl -w net.ipv4.ip_forward=1 && ufw disable && \
    ln -Tfs /usr/bin/python3 /usr/bin/python

apt-get update
apt-get install -y python3-distutils
apt-get install -y python3-pip

apt remove -y ansible
pip3 install -r kubespray/requirements.txt

git clone https://github.com/yaml/pyyaml.git
cd pyyaml
git checkout 5.4.1
python3 setup.py install
cd ../
rm -rf pyyaml

pip3 install awscli cloudpickle zmq protobuf==3.19.4 boto3 kubernetes six
