from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Business, BusinessImage, Service, BusinessHours, Category, BusinessRating, Message

class BusinessRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].label_from_instance = lambda obj: obj.name

    class Meta:
        model = Business
        fields = ['name', 'category', 'phone', 'instagram', 'description', 'address', 'city', 'district']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('مثال: میزبان')}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '09xxxxxxxxx'}),
            'instagram': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('نام کاربری اینستاگرام')}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': _('در مورد شغل خود توضیح دهید...')}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('آدرس کامل شامل خیابان، پلاک، واحد')}),
            'city': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('تهران', 'تهران'),
                ('مشهد', 'مشهد'),
                ('اصفهان', 'اصفهان'),
                ('کرج', 'کرج'),
                ('شیراز', 'شیراز'),
            ]),
            'district': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('منطقه یا محله')}),
        }
        labels = {
            'name': _('نام شغل'),
            'category': _('دسته‌بندی اصلی'),
            'phone': _('شماره تماس'),
            'instagram': _('آدرس اینستاگرام'),
            'description': _('توضیحات شغل'),
            'address': _('آدرس کامل'),
            'city': _('شهر'),
            'district': _('منطقه'),
        }

class BusinessImageForm(forms.ModelForm):
    class Meta:
        model = BusinessImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('نام سرویس')}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('مثال: fa-bullseye')}),
        }
        labels = {
            'name': _('نام سرویس'),
            'icon': _('آیکون (Font Awesome)'),
        }

class BusinessHoursForm(forms.ModelForm):
    class Meta:
        model = BusinessHours
        fields = ['days', 'start_time', 'end_time', 'is_closed']
        widgets = {
            'days': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.Select(attrs={'class': 'form-select'}),
            'end_time': forms.Select(attrs={'class': 'form-select'}),
            'is_closed': forms.CheckboxInput(),
        }

class BusinessRatingForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '۱ ستاره'),
        (2, '۲ ستاره'),
        (3, '۳ ستاره'),
        (4, '۴ ستاره'),
        (5, '۵ ستاره'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label=_('امتیاز')
    )
    
    class Meta:
        model = BusinessRating
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'placeholder': _('نظر خود را در مورد این کسب‌وکار بنویسید...'),
                'rows': 5
            }),
        }
        labels = {
            'comment': _('نظر'),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        return float(rating)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'message-input',
                'placeholder': _('پیام خود را بنویسید...'),
                'rows': 3
            }),
            'file': forms.ClearableFileInput(attrs={
                'accept': 'image/*,video/*,.pdf,.doc,.docx',
                'class': 'file-input'
            }),
        }
        labels = {
            'content': _('پیام'),
            'file': _('فایل'),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = file.content_type.split('/')[0]
            if file_type not in ['image', 'video', 'application']:
                raise forms.ValidationError(_('فقط تصاویر، ویدئوها و فایل‌های PDF/DOC/DOCX مجاز هستند.'))
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError(_('حجم فایل نباید بیشتر از ۱۰ مگابایت باشد.'))
            return file
        return None