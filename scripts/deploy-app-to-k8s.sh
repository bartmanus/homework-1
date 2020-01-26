#! /usr/bin/env bash

gcp_sa_key_file=gcp_sa_key.json
gcp_project=x-ripple-123456
gcp_location=europe-west3-c
gke_cluster=homework-1-gke-cluster
gsdk_url=https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-277.0.0-linux-x86_64.tar.gz
gsdk_sha256sum=b158894c427712d006fac235daf8d288db110ecfbcf649ed11cdf36ac2b2ff2a

curl -o gsdk.tar.gz $gsdk_url
test $(sha256sum gsdktar.gz | cut -d\  -f1) == ${gsdk_sha256sum} || exit
tar xzf gsdk.tar.gz
yes | bash google-cloud-sdk/install.sh
source google-cloud-sdk/path.bash.inc
yes | gcloud components update
yes | gcloud components install kubectl

gcloud auth activate-service-account --key-file=$gcp_sa_key_file
gcloud container clusters get-credentials $gke_cluster --project=$gcp_project --zone=$gcp_location

cat ../deploy/{deployment,service}.yaml | kubectl apply -f-

