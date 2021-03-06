from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # retrive post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data # retrive validated and clean data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


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





