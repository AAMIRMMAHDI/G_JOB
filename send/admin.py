from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Business, BusinessImage, Service, BusinessHours, BusinessRating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

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

    fieldsets = (
        (None, {
            'fields': (
                'owner', 'name', 'slug', 'category', 'phone', 'instagram',
                'description', 'address', 'city', 'district', 'is_approved'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'category')

    def approve_businesses(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, _(f"{updated} کسب‌وکار با موفقیت تأیید شدند."))
    approve_businesses.short_description = _("تأیید کسب‌وکارهای انتخاب‌شده")

    actions = [approve_businesses]

@admin.register(BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ('business', 'image', 'id')
    list_filter = ('business',)
    search_fields = ('business__name',)
    ordering = ('business',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('business', 'name', 'icon')
    list_filter = ('business',)
    search_fields = ('name', 'business__name', 'icon')
    ordering = ('business',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business')

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('business', 'days', 'start_time', 'end_time', 'is_closed')
    list_filter = ('business', 'is_closed')
    search_fields = ('business__name', 'days')
    ordering = ('business',)
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business')

@admin.register(BusinessRating)
class BusinessRatingAdmin(admin.ModelAdmin):
    list_display = ('business', 'user', 'rating', 'created_at')
    list_filter = ('business', 'rating', 'created_at')
    search_fields = ('business__name', 'user__username', 'comment')
    ordering = ('-created_at',)
    raw_id_fields = ('user',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('business', 'user', 'rating', 'comment')
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('business', 'user')
    



