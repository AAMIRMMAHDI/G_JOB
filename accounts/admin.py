from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Business

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'phone_number', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'city')
    search_fields = ('username', 'email', 'first_name', 'phone_number')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'email', 'phone_number', 'city', 'profile_picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'phone_number', 'city', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'views', 'rating', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'category', 'address')
    ordering = ('-created_at',)