from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from products.models import Product, ProductStatus, ProductCategory, ProductColor, Review
#                                                                    ^^^^ Color→ProductColor, Size o'chirildi


def product_list_view(request):
    products = Product.objects.filter(
        status=ProductStatus.ACTIVE
    ).prefetch_related(
        'images', 'categories', 'colors', 'reviews'
    ).order_by('-created_at')

    categories = ProductCategory.objects.filter(parent=None)
    colors = ProductColor.objects.all()  # Color → ProductColor
    # sizes = Size.objects.all()  # Size modeli yo'q, o'chirildi

    context = {
        "products": products,
        "categories": categories,
        "colors": colors,
        # "sizes": sizes,  # o'chirildi
    }
    return render(request, 'products/product-list.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(
        Product.objects.filter(
            status=ProductStatus.ACTIVE
        ).prefetch_related(
            'images', 'categories', 'colors', 'reviews'  # 'sizes' o'chirildi
        ),
        pk=pk
    )

    related_products = Product.objects.filter(
        status=ProductStatus.ACTIVE,
        categories__in=product.categories.all()
    ).exclude(
        pk=product.pk
    ).prefetch_related(
        'images', 'colors', 'reviews'
    ).distinct()[:8]

    main_image = product.images.filter(is_primary=True).first()  # is_main → is_primary
    if not main_image:
        main_image = product.images.first()

    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    context = {
        "product": product,
        "related_products": related_products,
        "main_image": main_image,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
        "review_count": reviews.count(),
        "categories": product.categories.all(),
    }
    return render(request, 'products/product.html', context)