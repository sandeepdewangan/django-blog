# Django
Docs for the book - Django 3 By Example

## REMEMBER

### Static Files
```
blog->static->css->blog.css
```
### Templates
```
blog->templates->blog->index.html
```

### Building URL
```python
<a href="{% url "blog:post_share" post.id %}">
```

## Python Basic Commands

1. Python version
```shell
$ python --version
```

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

## Custom Manager
`objects` is the default manager.

> Custom manager to retrieve all posts with the `published` status

`models.py`
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
    
    
class Post(models.Model):
    objects = models.Manager() # Default Manager
    published = PublishedManager() # Custom Manager
```
Using Custom Model
```python
 from blog.models import Post
 Post.published.filter(title__startswith='Who')
```


## View

Article List and Detail Page

```python
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post', post})
```

### URL Mapping
**Create urls.py inside blog** \
`url.py` of blog app

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
]
```

* Application namespace, allows to organize urls by application.
* `<int:year>` these all are path converters.
* if path converters is not sufficient use `re_path`.

**Edit urls.py inside main project directory**\
`urls.py` of main directory
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
]
```

## Canonical URL's
A Canonical URL's is a preferred URL for a resource.\
`models.py`
```python
from django.urls import reverse

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.date, self.slug])
```
* reverse() allows to build URL by their name and pass optional param.

## Templates

```
|--templates
|----blog
|------base.html
|------post
|--------list.html
|--------detail.html
```

**Template Tags**\
`{% tag %}` Renders template
**Template Variables**\
`{{ variable }}` Places values
**Template Filters**\
`{{ variable |filter }}` Modify variables

### Template Views
`base.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %} {% endblock %}</title>
    <link href="{% static 'css/blog.css' %}" rel="stylesheet">
</head>
<body>
<div id="content">
    {% block content %}
    {% endblock %}
</div>
</body>
</html>
```

* `{% load static %}` loads static template tags that are provided by the `django.contrib.staticfiles` app.
* `blog.css` is located under `blog/static/css` directory.

`list.html`

```python
{% extends "blog/base.html" %}
{% block title %} My Blog Home Page {% endblock %}
{% block content %}
    <h1>My Blog</h1>
    {% for post in posts %}
        <h2>
            <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
        </h2>
        <p class="date">
            Published {{ post.publish }} by {{ post.author }}
        </p>
        {{ post.body|truncatewords:30|linebreaks }}
    {% endfor %}
{% endblock %}
```

**Explaination - Custom URL**
1. `get_absolute_url` called from HTML which is defined in model class.
```python
# reverse() allows to build URL by their name and pass optional param.
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
```
2. The reverse method return custom url.
3. `blog` is app name and `post_detail` is view name. \
`urls.py`
```python
path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
```
`views.py`
```python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post', post})
```

### Contd.

`detail.html`
```python
{% extends 'blog/base.html' %}
{% block title %}{{ post.title }}{% endblock title %}

{% block content %}
    <h1> {{ post.title }}
    <p class="date">
        Published {{ post.publish }} by {{ post.author }}
    </p>
    {{ post.body|linebreaks }}
{% endblock content %}
```

## Pagination
Function Based Pagination and Class Based Pagination

### Function Based Pagination

1. Edit `view.py`
```python
def post_list(request):
    object_list = Post.published.all()
    # 1 - initialize the paginator class, 3 post in each page
    paginator = Paginator(object_list, 3)
    # 2 - get current page number
    page = request.GET.get('page')
    try:
        # 3 - obtain object for desired page
        posts = paginator.page(page) 
    except PageNotAnInteger:
        #if page not an integer deliver first page
        posts = paginator.page(1) 
    except EmptyPage:
        # if page is out of range deliver last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
```

2. Create `pagination.html`

```html
<div class="pagination">
  <span class="step-links">
    {% if page.has_previous %}
      <a href="?page={{ page.previous_page_number }}">Previous</a>
    {% endif %}
    <span class="current">
      Page {{ page.number }} of {{ page.paginator.num_pages }}.
    </span>
    {% if page.has_next %}
      <a href="?page={{ page.next_page_number }}">Next</a>
    {% endif %}
  </span>
</div>
```

3. Include pagination under `list.html`
```python
{% include "pagination.html" with page=posts %}
```


## Class Based Views and Class Based Pagination
Advantages of Class based views
1. Organizing code GET, POST, PUT in separate method.
2. Using multiple inheritance to create reusable view classes (also known as mixins)

**Create View**
```python
from django.views.generic import ListView
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
```

**Edit `urls.py`**
```python
path('', views.PostListView.as_view(), name='post_list'),
```

**Edit list.html**
> Django's ListView generic view passes the selected page in a variable called page_obj
```python
{% include "pagination.html" with page=page_obj %}
```