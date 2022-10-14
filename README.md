# Django Plugin For memberpress REST API Client

[![pypi django-memberpress-client](https://img.shields.io/static/v1?label=pypi&style=flat-square&color=0475b6&message=django-memberpress-client)](https://pypi.org/project/django-memberpress-client/) [![memberpress](https://img.shields.io/static/v1?label=memberpress&style=flat-square&color=04d4e4&message=REST%20API)](https://memberpress.com/addons/developer-tools/) [![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

![memberpress](https://memberpress.com/wp-content/uploads/2022/01/memberpress-logo-color.svg)

A lightweight, performant Django plugin that implements integrations to/from a ![Wordpress](https://wordpress.org/) ![memberpress](https://memberpress.com/) ![REST API](https://memberpress.com/blog/memberpress-developer-tools/#REST_API_Documentation) host.

## Installation

```bash
pip install django-memberpress-client
```

Set the Django settings using tutor.

```python
from django.conf import settings

settings.MEMBERPRESS_API_KEY = 'set-me-please'
settings.MEMBERPRESS_API_BASE_URL = 'https://set-me-please.com/'
```

You'll find the memberpress API Key in the Wordpress admin site.
![memberpress API Key](doc/memberpress-api-key.png "memberpress API Key")

## Usage

```python
from memberpress_client.member import Member

# 1. passing an explicit Wordpress username
member = Member(username="jsmith")
print(member.is_active_subscription)
print(member.is_trial_subscription)

# 2. using with Django request object
member = Member(request=request)

# 3. passing a Django user object
member = Member(user=user)

# 4. passing a Django user object
member = Member(user=user)

# 5. passing an json return object from memberpress REST API
member = Member(response=memberpress_response_json)
```


## Local development

* Use the same virtual environment that you use for edx-platform
* Set your Python interpreter to 3.8x
* install black: https://pypi.org/project/black/
* install flake8: https://flake8.pycqa.org/en/latest/

```bash
# Run these from within your edx-platform virtual environment
pip3 install pre-commit
pre-commit install
pip3 install black
python3 -m pip install flake8
```

### Local development good practices

* run `black` on modified code before committing.
* run `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
* run `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
* run `pre-commit run --all-files` before pushing. see: https://pre-commit.com/

#### edx-platform dependencies

To avoid freaky version conflicts in prod it's a good idea to install all of the edx-platform requirements to your local dev virtual environment.

* requirements/edx/base.txt
* requirements/edx/develop.txt,
* requirements/edx/testing.txt

At a minimum this will give you the full benefit of your IDE's linter.

#### Notes regarding development with macOS M1

1. To avoid problems with installing the edx-platform requirements, create your virtual environment with Python >= 3.9.x using the native installer from https://www.python.org/. `which python` should return `/Library/Frameworks/Python.framework/Versions/3.9/bin/python3`. Ignoring this advise will lead to very weird side effects. Note that this is true even though Lilac actually runs on Python 3.8.x

2. Best to install openssl, openblas, zstd, mysql, and mysql-client with Brew. Using brew helps you avoid problems with gcc compilations and linking that have proven problematic on early releases of macOS 11 on M1. If you run into problems while pip installing mysql-client / MongoDBProxy / mongoengine/ pymongo /numpy / scipy / matplotlib then analyze the stack trace for any other straggling dependencies that I might have ommitted here that might also break due to the gcc compiler or linker, and try installing these instead with Brew.

3. In addition to launching your virtual environment it also helps to set the following environment variables in your terminal window. Make sure you pay attention to any further suggestions echoed in Brew installation output:

```bash
export OPENBLAS=/opt/homebrew/opt/openblas/lib/
export LDFLAGS="-L/opt/homebrew/opt/openblas/lib -L/opt/homebrew/opt/mysql-client/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openblas/include -I/opt/homebrew/opt/mysql-client/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/openblas/lib/pkgconfig /opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

### Shell Plus and iPython

The stepwise_edxapi module adds ipython and django-extensions to the stack.  It is then possible to get an enhanced shell via:

```bash
tutor local exec lms ./manage.py lms shell_plus
```
