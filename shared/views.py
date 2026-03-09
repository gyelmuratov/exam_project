from django.contrib import messages
from django.shortcuts import render, redirect

from shared.models import (
    # Home
    AboutBanner,
    AboutSection,
    WhoWeAre,
    Testimonial,
    # About
    AboutPage,
    AboutPageBanner,
    Feature,
    Statistic,
    BrandSection,
    # Shared
    Brand,
    TeamMember,
    # Contact
    ContactBanner,
    ContactInfo,
    WorkingHours,
    Store,
    ContactMessage,
)

from products.models import Product, ProductStatus
from blogs.models import Blog, BlogStatus


def index_view(request):
    banner = AboutBanner.objects.filter(is_active=True).first()
    sections = AboutSection.objects.all()
    who_we_are = WhoWeAre.objects.filter(is_active=True).first()
    brands = Brand.objects.filter(is_active=True)
    team_members = TeamMember.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)

    featured_products = Product.objects.filter(
        status=ProductStatus.ACTIVE
    ).prefetch_related('images', 'colors', 'reviews').order_by('-created_at')[:8]

    latest_blogs = Blog.objects.filter(
        status=BlogStatus.PUBLISHED
    ).prefetch_related('authors', 'categories').order_by('-created_at')[:3]

    context = {
        "banner": banner,
        "sections": sections,
        "who_we_are": who_we_are,
        "brands": brands,
        "team_members": team_members,
        "testimonials": testimonials,
        "featured_products": featured_products,
        "latest_blogs": latest_blogs,
    }
    return render(request, 'shared/index.html', context)


def about_view(request):
    about = AboutPage.objects.filter(is_active=True).first()
    banner = AboutPageBanner.objects.filter(is_active=True).first()
    features = Feature.objects.filter(is_active=True)
    statistics = Statistic.objects.filter(is_active=True)
    team_members = TeamMember.objects.filter(is_active=True)
    brand_section = BrandSection.objects.filter(is_active=True).first()
    brands = Brand.objects.filter(is_active=True)

    context = {
        "about": about,
        "banner": banner,
        "features": features,
        "statistics": statistics,
        "team_members": team_members,
        "brand_section": brand_section,
        "brands": brands,
    }
    return render(request, 'shared/about.html', context)


def contact_view(request):
    banner = ContactBanner.objects.filter(is_active=True).first()
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    working_hours = WorkingHours.objects.all()
    stores = Store.objects.filter(is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message_text,
            )
            messages.success(request, "Xabaringiz yuborildi! Tez orada bog'lanamiz.")
            return redirect('shared:contact')
        else:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring.")

    context = {
        "banner": banner,
        "contact_info": contact_info,
        "working_hours": working_hours,
        "stores": stores,
    }
    return render(request, 'shared/contact.html', context)
