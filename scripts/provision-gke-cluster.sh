#! /usr/bin/env sh
pushd ../deploy/provision
pipenv install
GCP_AUTH_KIND=serviceaccount \
GCP_SA_KEY_FILE=gcp_sa_key.json \
GCP_LOCATION=europe-west3-c \
GCP_PROJECT=x-ripple-123456 \
GCP_CLUSTER_NAME=homework-1-gke-cluster \
pipenv run ansible-playbook gcloud-ansible-playbook.yml
popd
