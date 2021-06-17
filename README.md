# lambda-utility
[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![PyPi](https://img.shields.io/pypi/v/lambda-utility.svg)](https://pypi.org/project/lambda-utility/)


AWS Lambda에서 자주 사용하는 기능 구현

## Installation
Python 3.7 +
```bash
$ pip install lambda-utility
```

## Create a layer file
```bash
$ python layer

...
Complete -> 'lambda-utility.zip'
```
or
```bash
$ python layer -o {filename}

...
Complete -> '{filename}'
```
