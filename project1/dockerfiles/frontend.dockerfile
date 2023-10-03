FROM stalati/distributed-project1:base

MAINTAINER Sekwon Lee <stalati@utexas.edu> version: 0.1

USER root

WORKDIR $KVS_HOME

CMD python3 frontend.py
