#!/bin/bash

sudo docker image rm $(sudo docker image ls --format '{{.Repository}} {{.ID}}' | grep 'sekwonlee' | awk '{print $2}')

cd dockerfiles

sudo docker build . -f base.dockerfile -t sekwonlee/kvs:base
sudo docker push sekwonlee/kvs:base

sudo docker build . -f client.dockerfile -t sekwonlee/kvs:client
sudo docker push sekwonlee/kvs:client

sudo docker build . -f frontend.dockerfile -t sekwonlee/kvs:frontend
sudo docker push sekwonlee/kvs:frontend

sudo docker build . -f server.dockerfile -t sekwonlee/kvs:server
sudo docker push sekwonlee/kvs:server

cd ..
