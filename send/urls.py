from django.urls import path
from . import views

app_name = 'send'

urlpatterns = [
    path('', views.business_list_view, name='business_list'),
    path('send/register/', views.business_register_view, name='business_register'),
    path('send/business/<str:slug>/', views.business_detail_view, name='business_detail'),
    path('send/business/<str:slug>/review/', views.add_review_view, name='add_review'),
    path('send/business/<str:slug>/review/edit/', views.edit_review_view, name='edit_review'),
    path('send/business/<str:slug>/review/delete/', views.delete_review_view, name='delete_review'),
    path('send/business/<str:slug>/chat/', views.chat_view, name='chat'),
    path('send/chat/', views.chat_view, name='owner_chat'),
    path('send/messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
]