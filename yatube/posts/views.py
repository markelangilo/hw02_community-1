from .models import Post, Group

from django.shortcuts import get_object_or_404, render

from django.conf import settings 


def index(request):
    posts = Post.objects.all()[:settings.COUNT_POST]
    title = "Это главная страница проекта Yatube"
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()[:settings.COUNT_POST]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
