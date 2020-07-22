## Comment System

### STEP 01: Build Model
`model.py`
```python
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
	
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
```

 After defining related_name, you can retrieve the post of a comment object using comment.post and retrieve all comments of a post using post.comments.all(). If you don't define the related_name attribute, Django will use the name of the model in lowercase, followed by _set (that is, comment_set).

 ### STEP 02: Migrate
 ```bash
python manage.py makemigrations blog
python manage.py migrate
 ```

### STEP 03: Add to administrative site
`admin.py`
```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
```

### STEP 04: Forms for model
`forms.py`
```python
from django import forms
from .models import Comment

# Using Form
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

# Using ModelForm (Strongly binded with Model)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
```

### STEP 05: Handling form in views
`views.py`
```python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # list of active comments for the retrived post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid:
            new_comment = comment_form.save(commit=False)
            new_comment.post = post # assign current post to the comment
            new_comment.save() # save to db
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post' : post, 'comments': comments, 
                                        'new_comment': new_comment, 'comment_form': comment_form})
```

### STEP 06: Adding Comments to Post Detail Page
`post_detail`
```python
# comment Count
{% with comments.count as total_comments %}
        <h2>
            {{ total_comments }} comment{{ total_comments|pluralize }}
        </h2>
    {% endwith %}
# display all comments
    {% for comment in comments %}
        <div class="comment">
            <p class="info">
            Comment {{ forloop.counter }} by {{ comment.name }}
            {{ comment.created }}
            </p>
            {{ comment.body|linebreaks }}
        </div>
        {% empty %}
            <p>There are no comments yet.</p>
    {% endfor %}
# post comment
    {% if new_comment %}
        <h2>Your comment has been added.</h2>
        {% else %}
        <h2>Add a new comment</h2>
        <form method="post">
            {{ comment_form.as_p }}
            {% csrf_token %}
            <p><input type="submit" value="Add comment"></p>
        </form>
    {% endif %}
```
> NOTE: `comments.count()` is Django ORM in the template, executing the QuerySet. The {% with %} template tag is useful for avoiding hitting the database or accessing expensive methods multiple times.