from django.shortcuts import render


from blogs.models import BlogStatus, Category, Tag, Blog

def blogs_list_view(request):
    context = {
        "blogs": Blog.objects.filter(status=BlogStatus.PUBLISHED),
        "categories": Category.objects.filter(parent=None),
        "tags": Tag.objects.all(),
        "recent_posts": Blog.objects.order_by('-created_at')[:2]
    }
    return render(
        request, 'blogs/blogs-list.html',
        context
    )
