from django.urls import path
from . import views

app_name = 'send'

urlpatterns = [
    path('list', views.business_list_view, name='business_list'),
    path('register/', views.business_register_view, name='business_register'),
    path('business/<str:slug>/', views.business_detail_view, name='business_detail'),
    path('business/<str:slug>/review/', views.add_review_view, name='add_review'),
    path('business/<str:slug>/chat/', views.chat_view, name='chat'),
    path('chat/', views.chat_view, name='owner_chat'),
    path('messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
]