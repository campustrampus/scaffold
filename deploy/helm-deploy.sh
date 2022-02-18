#!/bin/sh

# Requried Environment Variables
# IMAGE_TAG - The image tag being applied to the deployed containers
# RELEASE_NAME - The name of Helm release
# CHART - The path to the Helm chart
# KUBE_CONTEXT - The kube context for the Kubernetes cluster
# SECRETS_FILE - Path of secrets file to be used
# VALUES_FILE - Path of values file to be used
# NAMESPACE - Kubernetes namespace that chart is being installed in

echo "Updating Helm Dependencies"
helm dep update ${CHART}

echo "Deploying Helm Release"
helm secrets upgrade \
${RELEASE_NAME} \
${CHART} \
--install \
--namespace ${NAMESPACE} \
--kube-context ${KUBE_CONTEXT} \
-f ${VALUES_FILE} \
-f ${SECRETS_FILE} \
--set backend.image.tag=${IMAGE_TAG} \
--set ui.image.tag=${IMAGE_TAG} \
--wait \
--timeout 15m \
--create-namespace
