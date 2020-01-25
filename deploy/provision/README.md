# Provision K8S cluster

Using Ansible, connect to Google Cloud and provision a container/GKE cluster
and a node pool.

__Warning__: Existence check seems to works on the level of cluster name,
added or changed properties are not applied.

Make sure environment variables contain proper values.

```bash
pushd deploy/provision/
GCP_AUTH_KIND=serviceaccount \
GCP_SA_KEY_FILE=/path/to/gcp_serviceaccount_credentials_file.json \
GCP_LOCATION=europe-west3-c \
GCP_PROJECT=x-ripple-123456 \
pipenv run ansible-playbook gcloud-ansible-playbook.yml
popd
```
