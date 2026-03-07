from django.db import models

from shared.models import BaseModel


class Author(BaseModel):
    full_name = models.CharField(
        max_length=255,
        verbose_name="Full Name",
    )
    about = models.CharField(
        max_length=255,
        verbose_name="About",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'authors'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Category(BaseModel):
    title = models.CharField(
        max_length=128,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True,
        verbose_name=("Parent category")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tag(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name="Title",
    )
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tags'
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class BlogStatus(models.TextChoices):
    PUBLISHED = "PUBLISHED", ("Published")
    DRAFT = "DRAFT", ("Draft")
    DELETED = "DELETED", ("Deleted")


class Blog(BaseModel):
    title = models.CharField(
        max_length=128,
        verbose_name="Title",
    )
    short_description = models.CharField(
        max_length=128,
        verbose_name="Short Description",
    )
    image = models.ImageField(
        upload_to='blogs/',
        null=True,
        blank=True,
        verbose_name=("Image")
    )
    long_description = models.TextField(
        verbose_name="Long Description",
    )
    status = models.CharField(
        max_length=20,
        choices=BlogStatus.choices,
        default=BlogStatus.DRAFT,
        verbose_name=("Status")
    )
    categories = models.ManyToManyField(
        Category,
        related_name='blogs',
        verbose_name=("Categories")
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='blogs',
        verbose_name=("Tags")
    )
    authors = models.ManyToManyField(
        Author,
        related_name='blogs',
        verbose_name=("Authors")
    )
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'