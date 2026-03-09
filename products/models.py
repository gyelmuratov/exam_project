from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from shared.models import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(
        max_length=128,
        verbose_name="Name",
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True,
        verbose_name="Parent category",
    )
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        verbose_name="Image",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_product_categories'  # o'zgartirildi
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class ProductTag(BaseModel):
    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_product_tags'  # o'zgartirildi
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"


class ProductColor(BaseModel):
    name = models.CharField(
        max_length=64,
        verbose_name="Name",
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name="Hex Code",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_product_colors'  # o'zgartirildi
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"


class Manufacture(BaseModel):
    name = models.CharField(
        max_length=128,
        verbose_name="Name",
    )
    country = models.CharField(
        max_length=64,
        verbose_name="Country",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'manufactures'
        verbose_name = "Manufacture"
        verbose_name_plural = "Manufactures"


class ProductStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DRAFT = 'draft', 'Draft'
    DELETED = 'deleted', 'Deleted'


class Product(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
    )
    sku = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="SKU",
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
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Main Image",
        null=True,
        blank=True,
    )

    # --- Narxlar ---
    price_uzs = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Price (UZS)",
    )
    discount_price_uzs = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Discount Price (UZS)",
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Price (USD)",
    )
    discount_price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Discount Price (USD)",
    )
    price_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Price (RUB)",
    )
    discount_price_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Discount Price (RUB)",
    )

    # --- Status ---
    status = models.CharField(
        max_length=16,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE,
        verbose_name="Status",
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Is Featured",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    # --- Relatsiyalar ---
    manufacture = models.ForeignKey(
        Manufacture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Manufacture",
    )
    categories = models.ManyToManyField(
        ProductCategory,
        related_name='products',
        blank=True,
        verbose_name="Categories",
    )
    tags = models.ManyToManyField(
        ProductTag,
        related_name='products',
        blank=True,
        verbose_name="Tags",
    )
    colors = models.ManyToManyField(
        ProductColor,
        through='ProductColorQuantity',
        related_name='products',
        blank=True,
        verbose_name="Colors",
    )

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        return sum(cq.quantity for cq in self.color_quantities.all())

    def get_main_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def get_review_count(self):
        return self.reviews.count()

    class Meta:
        db_table = 'store_products'  # o'zgartirildi
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductColorQuantity(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='color_quantities',
        verbose_name="Product",
    )
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        verbose_name="Color",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantity",
    )

    def __str__(self):
        return f"{self.product.name} - {self.color.name} ({self.quantity})"

    class Meta:
        db_table = 'store_product_color_quantities'  # o'zgartirildi
        verbose_name = "Product Color Quantity"
        verbose_name_plural = "Product Color Quantities"
        unique_together = ('product', 'color')


class ProductImage(BaseModel):
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
    alt_text = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Alt Text",
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Is Primary",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )

    def __str__(self):
        return f"{self.product.name} - image {self.order}"

    class Meta:
        db_table = 'store_product_images'  # o'zgartirildi
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order']


class Review(BaseModel):
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
        return f"{self.product.name} - {self.rating}★"

    class Meta:
        db_table = 'store_reviews'  # o'zgartirildi
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']