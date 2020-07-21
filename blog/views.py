from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


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
    return render(request, 'blog/post/detail.html', {'post' : post})




