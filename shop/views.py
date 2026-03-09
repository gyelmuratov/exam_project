from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import (
    Product, ProductStatus, ProductCategory,
    Size, Color, Brand, Review,
)


def product_list_view(request):
    products = Product.objects.filter(
        status=ProductStatus.ACTIVE
    ).prefetch_related('images', 'colors', 'categories', 'reviews')

    # --- Filters ---
    category_ids = request.GET.getlist('category')
    size_ids = request.GET.getlist('size')
    color_ids = request.GET.getlist('color')
    brand_ids = request.GET.getlist('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    sort_by = request.GET.get('sort', 'popular')

    if category_ids:
        products = products.filter(categories__id__in=category_ids).distinct()
    if size_ids:
        products = products.filter(sizes__id__in=size_ids).distinct()
    if color_ids:
        products = products.filter(colors__id__in=color_ids).distinct()
    if brand_ids:
        products = products.filter(brand__id__in=brand_ids).distinct()
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # --- Sort ---
    sort_options = {
        'popular':    '-created_at',
        'price_asc':  'price',
        'price_desc': '-price',
        'rating':     '-created_at',    # kelajakda annotate bilan
    }
    products = products.order_by(sort_options.get(sort_by, '-created_at'))

    total_count = products.count()

    # --- Pagination: 9 ta sahifada ---
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "total_count": total_count,
        "categories": ProductCategory.objects.filter(parent=None),
        "sizes": Size.objects.all(),
        "colors": Color.objects.all(),
        "brands": Brand.objects.all(),
        # Aktiv filterlar — checkbox uchun
        "selected_categories": [int(i) for i in category_ids if i.isdigit()],
        "selected_sizes": [int(i) for i in size_ids if i.isdigit()],
        "selected_colors": [int(i) for i in color_ids if i.isdigit()],
        "selected_brands": [int(i) for i in brand_ids if i.isdigit()],
        "price_min": price_min or 0,
        "price_max": price_max or 750,
        "sort_by": sort_by,
    }
    return render(request, 'shop/product-list.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(
        Product.objects.filter(status=ProductStatus.ACTIVE)
        .prefetch_related('images', 'colors', 'sizes', 'categories', 'reviews'),
        pk=pk,
    )

    # Ko'rishlar sonini oshirish (agar modelda bo'lsa)
    # Product.objects.filter(pk=pk).update(view_count=...)

    # Shu kategoriyadan o'xshash mahsulotlar
    category_ids = product.categories.values_list('id', flat=True)
    related_products = Product.objects.filter(
        status=ProductStatus.ACTIVE,
        categories__id__in=category_ids,
    ).exclude(pk=pk).prefetch_related('images', 'reviews').distinct()[:8]

    main_image = product.images.filter(is_main=True).first() or product.images.first()
    reviews = product.reviews.all()
    avg_rating = product.get_average_rating()
    review_count = product.get_review_count()

    # Review yuborish
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        rating = request.POST.get('rating', '').strip()
        comment = request.POST.get('comment', '').strip()

        if name and email and rating and comment:
            Review.objects.create(
                product=product,
                name=name,
                email=email,
                rating=int(rating),
                comment=comment,
            )

    context = {
        "product": product,
        "main_image": main_image,
        "related_products": related_products,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_count": review_count,
    }
    return render(request, 'shop/product-detail.html', context)
