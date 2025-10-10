from django.urls import path
from . import views

app_name = 'root'

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

]