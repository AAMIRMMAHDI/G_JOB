from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

        # 🔹 عنوان‌های فارسی فیلدها
        labels = {
            'name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'phone': 'شماره تماس',
            'subject': 'موضوع پیام',
            'message': 'متن پیام',
        }

        # 🔹 ظاهر و placeholder فیلدها
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'نام و نام خانوادگی خود را وارد کنید'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'example@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '09xxxxxxxxx'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'موضوع پیام خود را وارد کنید'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'متن پیام خود را بنویسید...'
            }),
        }
