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

To install the dependencies and run the app, ensure you have installed on your host:

* Python 3.7
* pipenv

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
pipenv run waitress-serve --listen '0.0.0.0:8080' --connection-limit=2000 --asyncore-use-poll --call 'homework:create_app'
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

