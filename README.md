# Django
Docs for the book - Django 3 By Example


## Python Basic Commands

1. Python version
```shell
$ python --version
```

2.


## Isolated Python Envirnment

**Step 01 - Create Envirnment**
```shell
$ python -m venv my_env
```

**Step 02 - Activate**
```shell
$ my_env\Scripts\activate
```

**Step 03 - De-activate**
```shell
$ deactivate
```

## Installing Django

```shell
$ pip install Django==3.0.*
```

Upgrading Pip

```shell
$ python -m pip install --upgrade pip
```

Getting Django Version

```shell
$ python
>>> import django
>>> django.get_version()
'3.0.8'
```

## Creating and Running Django Project

Create Project

```shell
$ django-admin startproject mysite
```

Start Server 
```shell
$ python manage.py runserver
```

Create Application
```shell
$ python manage.py startapp blog
```




## Migration
```shell
$ cd mysite
$ python manage.py migrate
```

## Settings

* Debug -> set it false when in production.
* USE_TZ -> activate/deactivate timezone support.

