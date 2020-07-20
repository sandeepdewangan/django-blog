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
  import django
  django.get_version()
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

Registering Application
`settings.py`
```python
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
]
```


## Migration
```shell
$ cd mysite
$ python manage.py makemigrations blog
$ python manage.py migrate
```

## Settings

* Debug -> set it false when in production.
* USE_TZ -> activate/deactivate timezone support.



## Models

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
```

* Reverse relationship is specified from User to Post using related_name attribute. (_ _ is used for accessing related models)
* auto_now_add -> date automatically added (while CREATE)
* auto_now -> date wil be updated automatically every time the object changes ((while UPDATE)
* Both auto_now_add and auto_now is not visible while filling form.



## Administrative Site
Create Super User
```shell
$ python manage.py createsuperuser
```

Adding Models to Administrative Site
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

Customizing Admin Site using Decorator

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
```

## Query Sets and Managers
Querysets is a collection of database quaries to retrive objects form db.

To open python shell for interacting with db use:
```shell script
$ python manage.py shell
```

Database Operations
---
### Create
```python
  from django.contrib.auth.models import User
  from blog.models import Post
  user = User.objects.get(username='sandeep')
  post = Post(title='new post', slug='new-post', body='Post body', author=user)
  post.save()
```
* get() retrive single object.
* save() used to persist records into db.

```python
  Post.objects.create(title='another', slug='another-new', body='newww', author=user)
```
* Need not need to call save() method.

### Update

```python
  post.title = 'New updated title'
  post.save()
```

### Retrive

```python
  all_posts = Post.objects.all()
```

Filter

```python
  Post.objects.filter(publish__year=2020)
```
Multiple Filter
```python
  Post.objects.filter(publish__year=2020, author__username='sandeep')
```

Exclude

```python
Post.objects.filter(publish__year=2020).exclude(title__startswith='Why')
```
Order By
```python
Post.objects.order_by('title') #ASC
Post.objects.order_by('-title') #DESC
```

### Delete

```python
 post = Post.objects.get(id=1)
 post.delete()
```