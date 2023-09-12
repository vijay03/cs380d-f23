#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Usage: ./create_cluster_object.sh path-to-ssh-key"
    echo ""
    echo "If no SSH key is specified, the default SSH key (~/.ssh/id_rsa) will be used."

    exit 1
fi

SSH_KEY=$1

cd $KVS_HOME/kubespray

sudo pip3 install -r requirements.txt
sudo pip3 uninstall pyOpenSSL

echo "Creating cluster object..."
ansible-playbook -i inventory/kvs_cluster/inventory.ini --become \
    --user=${USER_NAME} --become-user=root cluster.yml \
    --private-key=${SSH_KEY} -K

echo "Finish creating cluster objects..."

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

#sudo docker login

#sudo kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
#sudo kubectl create secret generic regcred --from-file=.dockerconfigjson=/root/.docker/config.json --type=kubernetes.io/dockerconfigjson
#sudo kubectl taint nodes master0 node-role.kubernetes.io/master:NoSchedule-
sudo kubectl label nodes master0 role=general

cd $KVS_HOME
