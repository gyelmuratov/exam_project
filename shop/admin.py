from django.contrib import admin

from .models import (
    ProductCategory,
    Size,
    Color,
    Brand,
    Product,
    ProductImage,
    Review,
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_product_count')
    list_filter = ('parent',)
    search_fields = ('title',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'hex_code')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'color', 'is_main')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('name', 'email', 'rating', 'comment', 'created_at')
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'old_price', 'label', 'status', 'brand', 'created_at')
    list_editable = ('status', 'label')
    list_filter = ('status', 'label', 'brand', 'categories')
    search_fields = ('title', 'short_description')
    filter_horizontal = ('categories', 'sizes', 'colors')
    inlines = (ProductImageInline, ReviewInline)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('name', 'email', 'product__title')
    readonly_fields = ('product', 'name', 'email', 'rating', 'comment', 'created_at')
