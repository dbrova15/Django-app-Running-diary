# Django-app: Running-diary
Django-application for running statistics.

###Technologies and Libraries:
\
Python3.7
\
Django==2.2.2
\
django-tables2==2.0.6
\
HTML/CSS
\
SQLite3
\
social-auth-app-django

###Prerequisites:

Needed to be installed Python3. If not installed, download the link https://www.python.org/ and install.

You need to create and fill in the file myapp/local_settings.py. An example of this file is myapp/local_settings_example.py. Fill in the database connection settings for production and for the test server.

###Deployment:
            
Run command:

```
pip3 install -r requirements.txt
```

Database Setup

```
python manage.py migrate
```

Create superuser

```
$ python manage.py createsuperuser
Username: admin
Email address: admin@admin.com
Password:
Password (again):
Superuser created successfully.
```

### Start app

```
python manage.py runserver
```