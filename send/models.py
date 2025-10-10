from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

class Business(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='businesses',
        verbose_name=_('Owner')
    )
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='businesses',
        verbose_name=_('Category')
    )
    description = models.TextField(verbose_name=_('Description'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('District'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Instagram'))
    is_approved = models.BooleanField(default=False, verbose_name=_('Is Approved'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            if not base_slug:
                base_slug = f"business-{Business.objects.count() + 1}"
            unique_slug = base_slug
            counter = 1
            while Business.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images', verbose_name=_('Business'))
    image = models.ImageField(upload_to='business_images/', verbose_name=_('Image'))

    class Meta:
        verbose_name = _('Business Image')
        verbose_name_plural = _('Business Images')

    def __str__(self):
        return f"Image for {self.business.name}"

class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services', verbose_name=_('Business'))
    name = models.CharField(max_length=50, verbose_name=_('Service Name'))
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Icon'), help_text=_('Font Awesome icon class, e.g., fa-bullseye'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.name

class BusinessHours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='hours', verbose_name=_('Business'))
    days = models.CharField(max_length=100, verbose_name=_('Days'))
    start_time = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('Start Time'))
    end_time = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('End Time'))
    is_closed = models.BooleanField(default=False, verbose_name=_('Is Closed'))

    class Meta:
        verbose_name = _('Business Hours')
        verbose_name_plural = _('Business Hours')

    def __str__(self):
        if self.is_closed:
            return f"{self.days}: تعطیل"
        return f"{self.days}: {self.start_time}-{self.end_time}"

class BusinessRating(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='ratings', verbose_name=_('Business'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    rating = models.FloatField(default=0.0, verbose_name=_('Rating'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comment'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Business Rating')
        verbose_name_plural = _('Business Ratings')
        unique_together = ['business', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.business.name}: {self.rating}"

    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)

class Conversation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='conversations', verbose_name=_('Business'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='conversations', verbose_name=_('User'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        unique_together = ['business', 'user']

    def __str__(self):
        return f"Conversation between {self.user.username} and {self.business.name}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Conversation'))
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('Sender'))
    content = models.TextField(verbose_name=_('Message Content'))
    file = models.FileField(upload_to='chat_files/', blank=True, null=True, verbose_name=_('File'))
    file_type = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('File Type'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation}"