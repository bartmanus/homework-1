# Homework

A simple dynamic web application in a CI/CD world.

## Web App

### Dependency Installation

Dependencies:

* `Flask` Python web framework
* the `waitress` production-level server.

Development specific:

* Pythonic wheel packaging tool `pbr`
* testing tools `pytest` and `coverage`

To install the dependencies and run the app, ensure you have the following 
tools installed on your host:

* Python, version >= 3.7
* pipenv, version >= 2018.11.26

Run:

```bash
pipenv install --dev
```

### Development Usage

This will start a foreground server process, occupying the shell:

```bash
FLASK_APP=homework FLASK_ENV=development pipenv run flask run
```

### Test the App

#### Black Box Testing

In a seprate shell invoke an ubiquitous HTTP client:

```bash
curl -i 'http://localhost:5000/dynamic'
```
Expect output similar to the below text:

```txt
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 19
Server: Werkzeug/0.16.0 Python/3.7.6
Date: Sun, 19 Jan 2020 17:09:42 GMT

0.29421629165877494
```

#### Built-in Tests

Run:

```bash
pipenv run coverage run -m pytest
pipenv run coverage report
```

You should see similar output to the following:

```txt
======================= test session starts =========================
platform linux -- Python 3.7.6, pytest-5.3.3, py-1.8.1, pluggy-0.13.1
rootdir: [redacted]/homework, inifile: setup.cfg, testpaths: tests
collected 3 items                                                                                                 

tests/test_dynamic.py ..                                       [ 66%]
tests/test_factory.py .                                        [100%]

======================= 3 passed in 40.11s ==========================
```

```txt
Name                   Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------
homework/__init__.py      21      0      2      0   100%
homework/dynamic.py        7      0      0      0   100%
--------------------------------------------------------
TOTAL                     28      0      2      0   100%

```

### Production Usage

Run the
[waitress server](https://docs.pylonsproject.org/projects/waitress/en/stable/arguments.html#arguments):

```bash
pipenv run waitress-serve --listen '0.0.0.0:8080' \
                          --connection-limit=2000 \
                          --asyncore-use-poll '
                          --call '
                          'homework:create_app'
```

```txt
> booting
> booted
Serving on http://0.0.0.0:8080
```

## Packaging Into a Wheel

Inspired by [@greut](https://medium.com/@greut/building-a-python-package-a-docker-image-using-pipenv-233d8793b6cc).
A wheel package can be built using:

```bash
pipenv run python setup.py bdist_wheel
tree dist/
```

```txt
dist/
└── homework-0.0.1.dev12-py3-none-any.whl
```

## Containerization

### Building an Image

Use your favourite build tool, e.g.:

```bash
docker build homework:latest .
podman build -t homework:latest --format docker .
buildah bud -t homework:latest --format docker .
```

### Running an Image

```bash
docker run --rm -d -p 8080:8080 homework:latest
podman run --rm -d -p 8080:8080 homework:latest
```

Test with an ubiquitous HTTP client like mentioned before.

## Cloudification

For some reason (gratis 300$ debit) Google Cloud was chosen to host the application.

Not everything on GCloud was automated:

* registering account
* enabling GKE service
* creating a project
* creating a service account for the project and issuing a deployment key for it

### Provision K8S Cluster

Automated using Ansible, but not part of CI. When Ansible is used against APIs,
it usually runs on localhost where some dependencies for the Ansible modules are
installed. Again, make sure these basic tools exist:

* Python, version >= 3.7
* pipenv, version >= 2018.11.26

Using Ansible, connect to Google Cloud and provision a container/GKE cluster
and a node pool. Make sure environment variables contain proper values.

__Warning__: Many properties cannot be changed after cluster creation.

```bash
pushd deploy/provision/
python3 -m pip install pipenv
pythin3 -m pipenv
GCP_AUTH_KIND=serviceaccount \
GCP_SA_KEY_FILE=/path/to/gcp_serviceaccount_credentials_file.json \
GCP_LOCATION=europe-west3-c \
GCP_PROJECT=x-ripple-123456 \
pipenv run ansible-playbook gcloud-ansible-playbook.yml
popd
```

### Apply K8S Deployment and Service Declarations

Some tools are required to interface with Google Cloud and the Kubernetes cluster.
Here's a shell script for installation using the basic tools `bash` and `curl`:

```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-277.0.0-linux-x86_64.tar.gz
test $(sha256sum google-cloud-sdk-277.0.0-linux-x86_64.tar.gz | cut -d\  -f1) == b158894c427712d006fac235daf8d288db110ecfbcf649ed11cdf36ac2b2ff2a || exit
tar xzf google-cloud-sdk-277.0.0-linux-x86_64.tar.gz
yes | bash google-cloud-sdk/install.sh
source google-cloud-sdk/path.bash.inc
yes | gcloud components update
yes | gcloud components install kubectl
```

Now create a kubectl configuration so it can auhtentication against the created
cluster. Some varible names are used below, see their definitionin the previous
chapter.

```bash
gcloud auth activate-service-account --key-file=$GCP_SA_KEY_FILE
gcloud container clusters get-credentials homework-1-gke-cluster --project=$GCP_PROJECT --zone=$GCP_LOCATION
```

Now the workload on the GKE cluser can finally be deployed and exposed:

```bash
cat deployment.yml service.yml | kubectl apply -f-
```

## Performance testing

The workload on GKE is exposed on by a Load Balancer IP. It can then receive
requests. To test performance, one can use a variety of tools,
e.g. ab, wrk, JMeter, tsung. Since this homework application is very simple and
has only a few resources, invoking the simple wrk for each is enough:

```bash
for url in http://${gke_service_ip}/{,dynamic}
do
    wrk -c 400 -d 60 --latency $url
done
```

Output:

```txt
Running 1m test @ http://35.234.75.59/
  2 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   313.29ms  107.43ms   1.97s    76.17%
    Req/Sec   604.71    381.79     1.98k    67.04%
  Latency Distribution
     50%  304.33ms
     75%  364.38ms
     90%  433.84ms
     99%  607.68ms
  71735 requests in 1.00m, 9.99MB read
  Socket errors: connect 0, read 0, write 0, timeout 203
Requests/sec:   1193.68
Transfer/sec:    170.19KB

Running 1m test @ http://35.234.75.59/dynamic
  2 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   300.49ms  107.46ms   1.98s    76.39%
    Req/Sec   649.85    428.48     2.05k    65.15%
  Latency Distribution
     50%  290.85ms
     75%  349.85ms
     90%  423.84ms
     99%  608.31ms
  76424 requests in 1.00m, 11.61MB read
  Socket errors: connect 0, read 0, write 0, timeout 145
Requests/sec:   1271.91
Transfer/sec:    197.83KB
```

