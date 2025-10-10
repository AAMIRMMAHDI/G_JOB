from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Phone Number'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name=_('Profile Picture'))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('City'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class Business(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_businesses', verbose_name=_('User'))
    name = models.CharField(max_length=200, verbose_name=_('Business Name'))
    category = models.CharField(max_length=100, verbose_name=_('Category'))
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Address'))
    views = models.PositiveIntegerField(default=0, verbose_name=_('Views'))
    rating = models.FloatField(default=0.0, verbose_name=_('Rating'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')

    def __str__(self):
        return self.name