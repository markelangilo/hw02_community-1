from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts_list,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    posts_count = author.posts.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'author': author,
               'posts_count': posts_count,
               'page_obj': page_obj}
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    posts_count = post.author.posts.count()
    title = post.text[:30]
    context = {'title': title,
               'post': post,
               'posts_count': posts_count}
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    select_group = Group.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author.username)
    else:
        form = PostForm()
    context = {
        'form': form,
        'title': 'Новая запись',
        'select_group': select_group
    }
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    select_group = Group.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author.username,)
    else:
        form = PostForm()
    context = {
        'form': form,
        'title': 'Новая запись',
        'is_edit': is_edit,
        'post': post,
        'select_group': select_group
    }
    return render(request, 'posts/create_post.html', context,)
