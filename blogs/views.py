from django.shortcuts import render, get_object_or_404

from .models import Blog, BlogStatus, Category, Tag


def blogs_list_view(request):
    blogs = Blog.objects.filter(
        status=BlogStatus.PUBLISHED
    ).prefetch_related(
        'authors', 'categories', 'tags'
    ).order_by('-created_at')

    categories = Category.objects.filter(parent=None)

    tags = Tag.objects.all()

    recent_posts = Blog.objects.filter(
        status=BlogStatus.PUBLISHED
    ).prefetch_related('authors').order_by('-created_at')[:5]

    context = {
        "blogs": blogs,
        "categories": categories,
        "tags": tags,
        "recent_posts": recent_posts,
    }
    return render(request, 'blogs/blogs.html', context)


def blog_detail_view(request, pk):
    blog = get_object_or_404(
        Blog.objects.filter(
            status=BlogStatus.PUBLISHED
        ).prefetch_related('categories', 'tags', 'authors'),
        pk=pk
    )

    # View countni oshirish
    Blog.objects.filter(pk=pk).update(view_count=blog.view_count + 1)

    recent_posts = Blog.objects.filter(
        status=BlogStatus.PUBLISHED
    ).exclude(
        pk=blog.pk
    ).prefetch_related('authors').order_by('-created_at')[:5]

    categories = Category.objects.filter(parent=None)

    tags = Tag.objects.all()

    context = {
        "blog": blog,
        "recent_posts": recent_posts,
        "categories": categories,
        "tags": tags,
    }
    return render(request, 'blogs/blog-detail.html', context)
