"""
URL configuration for core project.

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from send.sitemaps import StaticSitemap, BusinessSitemap
from .views import not_found_view


# تنظیمات sitemap
sitemaps = {
    'static': StaticSitemap,
    'businesses': BusinessSitemap,
}


urlpatterns = [
    # ادمین
    path('admin/', admin.site.urls),

    # اپ‌های اصلی
    path('', include('index.urls')),        # صفحه اصلی
    path('', include('send.urls')),         # کسب‌وکارها
    path('', include('accounts.urls')),     # احراز هویت

    # sitemap.xml — فقط content_type، تمپلیت خودش میاد
    path('sitemap.xml', sitemap, {
        'sitemaps': sitemaps,
        'content_type': 'text/xml',
    }, name='django_sitemap'),
]


# فقط در حالت توسعه (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^robots\.txt$', serve, {
            'document_root': settings.BASE_DIR / 'static',
            'path': 'robots.txt'
        }),
        re_path(r'^favicon\.ico$', serve, {
            'document_root': settings.BASE_DIR / 'static',
            'path': 'favicon.ico'
        }),
    ]


# 404 سفارشی — آخرین مورد (همه چیز رو می‌گیره)
urlpatterns += [
    re_path(r'^.*/?$', not_found_view, name='catch_all_404'),
]