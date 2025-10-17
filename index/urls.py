from django.urls import path
from . import views

app_name = 'root'

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('app/', views.app_page, name='app_page'),        # صفحه HTML
    path('app/download/', views.download_app, name='download_app'),  # دانلود فایل
]