from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    """فرم ورود"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input with-icon',
            'placeholder': _('نام کاربری'),
        }),
        label=_('نام کاربری')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input with-icon',
            'placeholder': _('رمز عبور'),
        }),
        label=_('رمز عبور')
    )

class RegisterForm(forms.ModelForm):
    """فرم ثبت‌نام"""
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input with-icon',
            'placeholder': _('رمز عبور'),
        }),
        label=_('رمز عبور')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input with-icon',
            'placeholder': _('تکرار رمز عبور'),
        }),
        label=_('تکرار رمز عبور')
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'phone_number', 'city']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': _('نام کاربری')}),
            'email': forms.EmailInput(attrs={'class': 'form-input with-icon', 'placeholder': _('ایمیل')}),
            'first_name': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': _('نام کامل')}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': '09xxxxxxxxx'}),
            'city': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': _('شهر')}),
        }
        labels = {
            'username': _('نام کاربری'),
            'email': _('ایمیل'),
            'first_name': _('نام کامل'),
            'phone_number': _('شماره تماس'),
            'city': _('شهر'),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('رمزهای عبور وارد شده مطابقت ندارند.'))
        return cleaned_data

class ProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'phone_number', 'city', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': _('نام کامل')}),
            'email': forms.EmailInput(attrs={'class': 'form-input with-icon', 'placeholder': _('ایمیل')}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': '09xxxxxxxxx'}),
            'city': forms.TextInput(attrs={'class': 'form-input with-icon', 'placeholder': _('شهر')}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'first_name': _('نام کامل'),
            'email': _('ایمیل'),
            'phone_number': _('شماره تماس'),
            'city': _('شهر'),
            'profile_picture': _('تصویر پروفایل'),
        }