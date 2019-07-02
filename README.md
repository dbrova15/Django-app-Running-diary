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

###Prerequisites
Needed to be installed Python3. If not installed, download the link https://www.python.org/ and install.

###Deployment:
If you are deploying a project on the server, specify the settings for connecting to the database in the file
            myapp.settings in the DATABASES dictionary.
            
Run command:

```
pip3 install -r requirements.txt
```

Database Setup

```
python manage.py migrate
```

### Start app

```
python manage.py runserver
```