#!/bin/bash

sudo docker image rm $(sudo docker image ls --format '{{.Repository}} {{.ID}}' | grep 'stalati' | awk '{print $2}')

cd dockerfiles

sudo docker build . -f base.dockerfile -t stalati/distributed-project1:base --network=host
sudo docker push stalati/distributed-project1:base

sudo docker build . -f client.dockerfile -t stalati/distributed-project1:client --network=host
sudo docker push stalati/distributed-project1:client

sudo docker build . -f frontend.dockerfile -t stalati/distributed-project1:frontend --network=host
sudo docker push stalati/distributed-project1:frontend

sudo docker build . -f server.dockerfile -t stalati/distributed-project1:server --network=host
sudo docker push stalati/distributed-project1:server

cd ..
