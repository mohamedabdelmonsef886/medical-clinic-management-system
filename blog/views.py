from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost

def blog_list(request):
    """Display all blog posts"""
    posts = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    """Display blog post detail"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'blog/blog_detail.html', {'post': post})