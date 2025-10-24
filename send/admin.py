from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Business, BusinessImage, Service, BusinessHours, BusinessRating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at',)

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category', 'city', 'slug', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'city', 'category', 'created_at')
    search_fields = ('name', 'description', 'owner__username', 'phone', 'slug')
    list_editable = ('is_approved',)
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['owner', 'category']
    list_per_page = 20
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'category')

    def approve_businesses(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, _(f"{updated} کسب‌وکار با موفقیت تأیید شدند."))
    approve_businesses.short_description = _("تأیید کسب‌وکارهای انتخاب‌شده")
    actions = [approve_businesses]




@admin.register(BusinessRating)
class BusinessRatingAdmin(admin.ModelAdmin):
    list_display = ('business_link', 'user_link', 'rating_stars', 'comment_preview', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at', 'business__category', 'business__city')
    search_fields = ('business__name', 'user__username', 'comment')
    list_editable = ('is_approved',)
    ordering = ('-created_at',)
    raw_id_fields = ('user',)
    list_per_page = 25
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('business', 'user', 'rating', 'comment', 'is_approved')
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business', 'user', 'business__category')

    def business_link(self, obj):
        url = reverse("admin:send_business_change", args=[obj.business.id])
        return format_html('<a href="{}">{}</a>', url, obj.business.name)
    business_link.short_description = _('Business')

    def user_link(self, obj):
        url = reverse("admin:accounts_customuser_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = _('User')
    def rating_stars(self, obj):
        full = int(obj.rating)
        half = 1 if obj.rating - full >= 0.5 else 0
        empty = 5 - full - half
        stars = '★' * full + '½' * half + '☆' * empty
        return format_html('<span style="color: #f39c12; font-size: 1.2em;">{}</span>', stars)
    rating_stars.short_description = _('Rating')

    def comment_preview(self, obj):
        if not obj.comment:
            return format_html('<span style="color: #999;">— بدون نظر —</span>')
        text = obj.comment.replace('\n', ' ').strip()
        preview = text[:97] + '...' if len(text) > 100 else text
        return format_html('<span title="{}">{}</span>', text, preview)
    comment_preview.short_description = _('Comment')

    def approve_ratings(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, _(f"{updated} نظر با موفقیت تأیید شد."))
    approve_ratings.short_description = _("تأیید نظرات انتخاب‌شده")
    actions = [approve_ratings]