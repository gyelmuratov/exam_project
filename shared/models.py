from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at"
    )

    class Meta:
        abstract = True


# ==================== HOME ====================

class HeroBanner(BaseModel):
    """Bosh sahifadagi asosiy slider/banner"""
    image = models.ImageField(
        upload_to='hero/',
        verbose_name="Image",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Title",
        null=True,
        blank=True,
    )
    subtitle = models.CharField(
        max_length=255,
        verbose_name="Subtitle",
        null=True,
        blank=True,
    )
    button_text = models.CharField(
        max_length=64,
        verbose_name="Button Text",
        null=True,
        blank=True,
    )
    button_url = models.CharField(
        max_length=255,
        verbose_name="Button URL",
        null=True,
        blank=True,
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title or f"Banner {self.pk}"

    class Meta:
        db_table = 'hero_banners'
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banners"
        ordering = ['order']


class HomeSection(BaseModel):
    """Index sahifasining har bir bo'limini yoqish/o'chirish uchun sozlamalar"""
    show_about_banner = models.BooleanField(default=True)
    show_vision_mission = models.BooleanField(default=True)
    show_who_we_are = models.BooleanField(default=True)
    show_brands = models.BooleanField(default=True)
    show_team = models.BooleanField(default=True)
    show_testimonials = models.BooleanField(default=True)
    show_featured_products = models.BooleanField(default=True)
    show_latest_blogs = models.BooleanField(default=True)

    def __str__(self):
        return "Home Page Settings"

    class Meta:
        db_table = 'home_settings'
        verbose_name = "Home Settings"
        verbose_name_plural = "Home Settings"


# ==================== ABOUT ====================

class AboutBanner(BaseModel):
    """About us sahifasidagi katta banner rasm"""
    image = models.ImageField(
        upload_to='about/',
        verbose_name="Banner Image",
    )
    title = models.CharField(
        max_length=128,
        verbose_name="Title",        # "About us"
    )
    subtitle = models.CharField(
        max_length=128,
        verbose_name="Subtitle",     # "Who we are"
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'about_banners'
        verbose_name = "About Banner"
        verbose_name_plural = "About Banners"


class AboutSection(BaseModel):
    """Our Vision / Our Mission qismi"""
    title = models.CharField(
        max_length=128,
        verbose_name="Title",        # "Our Vision"
    )
    description = models.TextField(
        verbose_name="Description",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'about_sections'
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"
        ordering = ['order']


class AboutPage(BaseModel):
    """About us 2 — Who We Are matn va imzo"""
    title = models.CharField(
        max_length=128,
        verbose_name="Title",        # "Who We Are"
    )
    description = models.TextField(
        verbose_name="Description",
    )
    signature = models.ImageField(
        upload_to='about/',
        verbose_name="Signature Image",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'about_page'
        verbose_name = "About Page"
        verbose_name_plural = "About Pages"


class AboutPageBanner(BaseModel):
    """'every day since 91' — katta background rasmli banner"""
    image = models.ImageField(
        upload_to='about/',
        verbose_name="Background Image",
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Text",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.text or f"About Page Banner {self.pk}"

    class Meta:
        db_table = 'about_page_banners'
        verbose_name = "About Page Banner"
        verbose_name_plural = "About Page Banners"


class WhoWeAre(BaseModel):
    """Who We Are qismi — chap matn, o'ng rasmlar"""
    title = models.CharField(
        max_length=128,
        verbose_name="Title",        # "Who We Are"
    )
    subtitle = models.CharField(
        max_length=255,
        verbose_name="Subtitle",     # sariq matn
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Description",
    )
    image_main = models.ImageField(
        upload_to='about/who-we-are/',
        verbose_name="Main Image",
        null=True,
        blank=True,
    )
    image_secondary = models.ImageField(
        upload_to='about/who-we-are/',
        verbose_name="Secondary Image",
        null=True,
        blank=True,
    )
    button_text = models.CharField(
        max_length=64,
        default="VIEW OUR NEWS",
        verbose_name="Button Text",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'who_we_are'
        verbose_name = "Who We Are"
        verbose_name_plural = "Who We Are"


class Feature(BaseModel):
    """Design Quality / Professional Support / Made With Love"""
    icon_class = models.CharField(
        max_length=64,
        verbose_name="Icon Class",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=128,
        verbose_name="Title",
    )
    description = models.TextField(
        verbose_name="Description",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'features'
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        ordering = ['order']


class Statistic(BaseModel):
    """40k+ Happy Customer / 20+ Years in Business"""
    value = models.CharField(
        max_length=32,
        verbose_name="Value",        # "40k+"
    )
    label = models.CharField(
        max_length=128,
        verbose_name="Label",        # "Happy Customer"
    )
    background_image = models.ImageField(
        upload_to='about/',
        verbose_name="Background Image",
        null=True,
        blank=True,
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return f"{self.value} {self.label}"

    class Meta:
        db_table = 'statistics'
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"
        ordering = ['order']


class Brand(BaseModel):
    """The world's premium design brands — logo grid"""
    title = models.CharField(
        max_length=128,
        verbose_name="Brand Name",
    )
    logo = models.ImageField(
        upload_to='brands/',
        verbose_name="Logo",
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name="Website URL",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'brands'
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['order']


class BrandSection(BaseModel):
    """Brands qismidagi sarlavha va tavsif"""
    title = models.CharField(
        max_length=255,
        verbose_name="Title",
    )
    description = models.TextField(
        verbose_name="Description",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'brand_section'
        verbose_name = "Brand Section"
        verbose_name_plural = "Brand Sections"


class TeamMember(BaseModel):
    """Meet Our Team qismi"""
    full_name = models.CharField(
        max_length=128,
        verbose_name="Full Name",    # "Samanta Grey"
    )
    position = models.CharField(
        max_length=128,
        verbose_name="Position",     # "Founder & CEO"
    )
    bio = models.TextField(
        verbose_name="Bio",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='team/',
        verbose_name="Image",
    )
    facebook = models.URLField(
        null=True,
        blank=True,
        verbose_name="Facebook",
    )
    twitter = models.URLField(
        null=True,
        blank=True,
        verbose_name="Twitter",
    )
    instagram = models.URLField(
        null=True,
        blank=True,
        verbose_name="Instagram",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'team_members'
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order']


class Testimonial(BaseModel):
    """What Customer Say About Us — carousel"""
    full_name = models.CharField(
        max_length=128,
        verbose_name="Full Name",    # "Jenson Gregory"
    )
    role = models.CharField(
        max_length=128,
        verbose_name="Role",         # "Customer"
        null=True,
        blank=True,
    )
    comment = models.TextField(
        verbose_name="Comment",
    )
    image = models.ImageField(
        upload_to='testimonials/',
        verbose_name="Photo",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'testimonials'
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['order']


# ==================== CONTACT ====================

class ContactBanner(BaseModel):
    """Contact us sahifasidagi katta banner"""
    image = models.ImageField(
        upload_to='contact/',
        verbose_name="Banner Image",
    )
    title = models.CharField(
        max_length=128,
        verbose_name="Title",           # "Contact us"
    )
    subtitle = models.CharField(
        max_length=128,
        verbose_name="Subtitle",        # "keep in touch with us"
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'contact_banners'
        verbose_name = "Contact Banner"
        verbose_name_plural = "Contact Banners"


class ContactInfo(BaseModel):
    """Contact Information — manzil, telefon, email"""
    title = models.CharField(
        max_length=128,
        verbose_name="Title",           # "Contact Information"
    )
    description = models.TextField(
        verbose_name="Description",
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Address",
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=32,
        verbose_name="Phone",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name="Email",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'contact_info'
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"


class WorkingHours(BaseModel):
    """The Office — ish vaqtlari"""
    day = models.CharField(
        max_length=64,
        verbose_name="Day",             # "Monday-Saturday"
    )
    hours = models.CharField(
        max_length=64,
        verbose_name="Hours",           # "11am-7pm ET"
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )

    def __str__(self):
        return f"{self.day}: {self.hours}"

    class Meta:
        db_table = 'working_hours'
        verbose_name = "Working Hours"
        verbose_name_plural = "Working Hours"
        ordering = ['order']


class Store(BaseModel):
    """Our Stores"""
    name = models.CharField(
        max_length=128,
        verbose_name="Store Name",      # "Wall Street Plaza"
    )
    image = models.ImageField(
        upload_to='stores/',
        verbose_name="Image",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Address",
    )
    phone = models.CharField(
        max_length=32,
        verbose_name="Phone",
        null=True,
        blank=True,
    )
    working_hours = models.TextField(
        verbose_name="Working Hours",
        null=True,
        blank=True,
    )
    map_url = models.URLField(
        verbose_name="Map URL",
        null=True,
        blank=True,
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitude",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Order",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stores'
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['order']


class ContactMessage(BaseModel):
    """Got Any Questions? — yuborilgan xabarlar"""
    name = models.CharField(
        max_length=128,
        verbose_name="Name",
    )
    email = models.EmailField(
        verbose_name="Email",
    )
    phone = models.CharField(
        max_length=32,
        verbose_name="Phone",
        null=True,
        blank=True,
    )
    subject = models.CharField(
        max_length=255,
        verbose_name="Subject",
        null=True,
        blank=True,
    )
    message = models.TextField(
        verbose_name="Message",
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Is Read",
    )

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"

    class Meta:
        db_table = 'contact_messages'
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
