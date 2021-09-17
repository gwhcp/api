# GWHCP - API

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