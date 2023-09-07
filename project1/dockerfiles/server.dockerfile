FROM sekwonlee/kvs:base

MAINTAINER Sekwon Lee <sklee@cs.utexas.edu> version: 0.1

USER root

WORKDIR $KVS_HOME

CMD python3 server.py -i $SERVER_ID
