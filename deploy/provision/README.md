# Provision K8S cluster

Using Ansible, connect to Google Cloud and provision a container/GKE cluster.

Make sure environment variables contain proper values.

```bash
GCP_AUTH_KIND=serviceaccount GCP_SA_KEY_FILE=/path/to/gcp_serviceaccount_credentials_file.json GCP_LOCATION=europe-west3-c GCP_PROJECT=x-ripple-123456 pipenv run ansible-playbook gcloud-ansible-playbook.yml
```
