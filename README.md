# Homework

A simple dynamic web application in a CI/CD world.

## Web App

### Dependency Installation

The Flask Python web framework is used.

To install the dependencies and run the app, ensure you have installed on your host:

* Python 3.7
* pipenv

Run:

```bash
pipenv install
```

### Run The App

This will start a foreground server process, occupying the shell:

```bash
FLASK_APP=homework FLASK_ENV=development pipenv run flask run
```

### Test the App

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

