# Identity API

[![Build Status](https://travis-ci.org/alexsdutton/idm-core.svg?branch=master)](https://travis-ci.org/alexsdutton/idm-core) [![codecov](https://codecov.io/gh/alexsdutton/idm-core/branch/master/graph/badge.svg)](https://codecov.io/gh/alexsdutton/idm-core)

A prototypical identity API supporting:

* Names (and not just first/last)
* Nationalities
* Affiliations and roles
* Gender
* Source documents, and the personal information they attest
* Publishing data changes to AMQP


# Getting started

Make rabbitmq available on localhost with a `guest:guest` administrator account.

    mkvirtualenv oxidentity --python=/usr/bin/python3
    pip install -r requirements

    createdb oxidentity
    django-admin.py migrate

    # Set a celery worker going
    celery -B -A oxidentity worker -l info &

    # Run the dev server
    django-admin.py runserver

    # Create a new identity
    curl http://localhost:8000/identity/ -d@examples/lewis-carroll.json -v
