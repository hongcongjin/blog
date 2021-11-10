from django.shortcuts import render

# Create your views here.
import markdown
import re
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify


def index(request):
    # return HttpResponse("欢迎访问我的博客首页！")
    # return render(request, 'blog1/index.html', context={
    #     'title':'我的博客首页',
    #     'welcome':'欢迎访问我的博客首页'
    # })
    post_list = Post.objects.all().order_by('-create_time')
    print(len(post_list))
    return render(request, 'blog1/index.html',
                  context={'post_list': post_list})


def detail(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    # return render(request, 'blog1/detail.html', context={'post': post})
    # post = get_object_or_404(Post, pk=pk)
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc'
    #                               ])
    # return render(request, 'blog1/detail.html', context={'post': post})
    # post = get_object_or_404(Post, pk=pk)
    # md = markdown.Markdown(extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # ])
    # post.body = md.convert(post.body)
    # post.toc = md.toc
    # return render(request, 'blog1/detail.html', context={'post': post})

    # post = get_object_or_404(Post, pk=pk)
    # md = markdown.Markdown(extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # ])
    # post.body = md.convert(post.body)
    #
    # m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    # post.toc = m.group(1) if m is not None else ''
    #
    # return render(request, 'blog1/detail.html', context={'post': post})

    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog1/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month).order_by(
        '-create_time')
    return render(request, 'blog1/index.html',
                  context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog1/index.html',
                  context={'post_list': post_list})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-create_time')
    return render(request, 'blog1/index.html',
                  context={'post_list': post_list})
