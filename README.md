
# SFDS formio-db-microservice.py [![CircleCI](https://circleci.com/gh/SFDigitalServices/formio-db-microservice.svg?style=svg)](https://circleci.com/gh/SFDigitalServices/formio-db-microservice) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/formio-db-microservice/badge.svg?branch=main)](https://coveralls.io/github/SFDigitalServices/formio-db-microservice?branch=main)
SFDS formio-ds-microservice was developed for CCSF to store data in secure databases.

## Requirements
* Python3
([Mac OS X](https://docs.python-guide.org/starting/install3/osx/) / [Windows](https://www.stuartellis.name/articles/python-development-windows/))
* Pipenv & Virtual Environments ([virtualenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))
* [Postgres](https://www.postgresql.org)
* [Redis](https://redis.io)

## Get started

Install Postgres (if needed)
*(with Homebrew)*
> $ brew install postgresql

Create database
> $ createdb formi_db_microservice

Create form table
> # see services/resources/models.py for table structure and create it locally

Install Redis (if needed)
*(with Homebrew)*
> $ brew install redis

Set Postgresql and Redis connection string environment variables
> $ export DATABASE\_URL=postgresql://localhost/formio\_db\_microservice

> $ export REDIS_URL=redis://localhost:6379

Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install --dev

*If you get a psycopg2 error, it may be due to the install being unable to find openssl libraries installed via homebrew.  Try the following command:*
> $ env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pipenv install --dev

Set ACCESS_KEY environment var and start WSGI Server
> $ ACCESS_KEY=123456 pipenv run gunicorn 'service.microservice:start_service()'

Run Pytest
> $ pipenv run python -m pytest

Get code coverage report
> $ pipenv run python -m pytest --cov=service --cov=tasks tests/ --cov-fail-under=90

Open with cURL or web browser
> $ curl --header "ACCESS_KEY: 123456" http://127.0.0.1:8000/welcome

## Development
Auto-reload on code changes
> $ ACCESS_KEY=123456 pipenv run gunicorn --reload 'service.microservice:start_service()'

Code coverage command with missing statement line numbers
> $ pipenv run python -m pytest --cov=service --cov=tasks tests/ --cov-report term-missing

Set up git hook scripts with pre-commit
> $ pipenv run pre-commit install

### Run Dev Server with SSL
Generate SSL keys
> $ openssl req -newkey rsa:2048 -nodes -keyout myserver-dev.key -x509 -out myserver-dev.crt

Run server with SSL keys
> $ ACCESS_KEY=123456 pipenv run gunicorn --reload --certfile=myserver-dev.crt --keyfile=myserver-dev.key -- bind 0.0.0.0:443 'service.microservice:start_service()'

## Continuous integration
* CircleCI builds fail when trying to run coveralls.
    1. Log into coveralls.io to obtain the coverall token for your repo.
    2. Create an environment variable in CircleCI with the name COVERALLS_REPO_TOKEN and the coverall token value.

## Heroku Integration
* Set ACCESS_TOKEN environment variable and pass it as a header in requests
