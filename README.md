# GWHCP - API

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/gwhcp/api.svg?branch=master)](https://travis-ci.com/gwhcp/api)

An open source web hosting control panel. Designed to be easy to use and highly customizable.

### Create Migrations
```
python manage.py makemigrations
```

### Create Database Tables
```
python manage.py migrate
python manage.py migrate xmpp --database xmpp
```

### Create Super User
```
python manage.py createsuperuser
```

### Remove all Migrations - Testing only
```
cd /e/PycharmProjects/gwhcp/api/gwhcp_api
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
```

### Start Server
```
python manage.py runserver <ipaddress>:<port>
```