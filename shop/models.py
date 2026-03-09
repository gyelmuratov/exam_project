from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from shared.models import BaseModel


class ProductCategory(BaseModel):
    """Category filter — Dresses, T-shirts, Bags, Jackets..."""
    title = models.CharField(
        max_length=128,
        verbose_name="Title",
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Parent Category",
    )
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        verbose_name="Image",
    )

    def __str__(self):
        return self.title

    def get_product_count(self):
        return self.products.filter(status=ProductStatus.ACTIVE).count()

    class Meta:
        db_table = 'product_categories'
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Size(BaseModel):
    """Size filter — XS, S, M, L, XL, XXL"""
    title = models.CharField(
        max_length=8,
        verbose_name="Size",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'sizes'
        verbose_name = "Size"
        verbose_name_plural = "Sizes"


class Color(BaseModel):
    """Colour filter — rang doiralar"""
    title = models.CharField(
        max_length=64,
        verbose_name="Color Name",
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name="Hex Code",        # "#FF0000"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'colors'
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class Brand(BaseModel):
    """Brand filter — Next, River Island, Geox, New Balance..."""
    title = models.CharField(
        max_length=128,
        verbose_name="Brand Name",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product_brands'
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class ProductLabel(models.TextChoices):
    NEW = 'new', 'New'
    OUT_OF_STOCK = 'out_of_stock', 'Out of Stock'
    SALE = 'sale', 'Sale'
    TOP = 'top', 'Top'
    NONE = 'none', 'None'


class ProductStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DRAFT = 'draft', 'Draft'
    DELETED = 'deleted', 'Deleted'


class Product(BaseModel):
    """Asosiy mahsulot modeli"""
    title = models.CharField(
        max_length=255,
        verbose_name="Title",
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name="Short Description",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Description",
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Old Price",       # SALE uchun
    )
    status = models.CharField(
        max_length=16,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE,
        verbose_name="Status",
    )
    label = models.CharField(
        max_length=16,
        choices=ProductLabel.choices,
        default=ProductLabel.NONE,
        verbose_name="Label",           # New / Out of Stock / Sale
    )
    categories = models.ManyToManyField(
        ProductCategory,
        related_name='products',
        blank=True,
        verbose_name="Categories",
    )
    sizes = models.ManyToManyField(
        Size,
        related_name='products',
        blank=True,
        verbose_name="Sizes",
    )
    colors = models.ManyToManyField(
        Color,
        related_name='products',
        blank=True,
        verbose_name="Colors",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Brand",
    )

    def __str__(self):
        return self.title

    def get_main_image(self):
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    def get_average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(r.rating for r in reviews) / reviews.count()

    def get_review_count(self):
        return self.reviews.count()

    def get_discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    class Meta:
        db_table = 'products'
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(BaseModel):
    """Mahsulot rasmlari — color variant thumbnails"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Product",
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Image",
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Is Main",
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
        verbose_name="Color",
    )

    def __str__(self):
        return f"{self.product.title} - image"

    class Meta:
        db_table = 'product_images'
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class Review(BaseModel):
    """Mahsulot sharhlari — (2 Reviews)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Product",
    )
    name = models.CharField(
        max_length=128,
        verbose_name="Name",
    )
    email = models.EmailField(
        verbose_name="Email",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating",
    )
    comment = models.TextField(
        verbose_name="Comment",
    )

    def __str__(self):
        return f"{self.product.title} - {self.name} ({self.rating}★)"

    class Meta:
        db_table = 'product_reviews'
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
