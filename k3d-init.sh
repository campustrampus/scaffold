#!/bin/bash
IMAGE='rancher/k3s:v1.21.2-k3s1'
NETWORK_NAME='k3d'
SUBNET='192.168.105.0/24'

# Create Docker Network
if ! docker network ls --format '{{json .Name }}' | grep -q ${NETWORK_NAME} ; then
	echo "Creating kind docker network"
	docker network create --subnet=${SUBNET} ${NETWORK_NAME}	
else
	echo "${NETWORK_NAME} docker network found"
fi

# Create Cluster
echo "creating cluster"
k3d cluster create \
${PROJECT_NAME} \
--image ${IMAGE} \
--network ${NETWORK_NAME} \
--no-lb \
--registry-create
