from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Business
from datetime import datetime

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'http'
    domain = '127.0.0.1:8000'  # چون رو لوکال‌هاست تست می‌کنی

    def items(self):
        return [
            'root:about',
            'root:contact',
            'root:app_page',
            'send:business_list',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return datetime.now()

class BusinessSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    protocol = 'http'
    domain = '127.0.0.1:8000'

    def items(self):
        return Business.objects.filter(is_approved=True).order_by('-created_at')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.created_at