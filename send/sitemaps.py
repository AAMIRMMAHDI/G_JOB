# send/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Business

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'root:about',
            'root:contact',
            'root:app_page',
            'send:business_list',
        ]

    def location(self, item):
        return reverse(item)

class BusinessSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Business.objects.filter(is_approved=True).order_by('-created_at')

    def location(self, obj):
        return obj.get_absolute_url()