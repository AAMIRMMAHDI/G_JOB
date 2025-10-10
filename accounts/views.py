from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Avg
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import Business

def login_view(request):
    """نمایش و مدیریت فرم ورود"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('✅ با موفقیت وارد شدید!'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('❌ نام کاربری یا رمز عبور اشتباه است.'))
    else:
        form = LoginForm()

    return render(request, 'accounts/LOGIN.html', {
        'login_form': form,
        'register_form': RegisterForm()
    })

def register_view(request):
    """نمایش و مدیریت فرم ثبت‌نام"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, _('🎉 ثبت‌نام با موفقیت انجام شد!'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('⚠️ لطفاً خطاهای فرم را برطرف کنید.'))
    else:
        form = RegisterForm()

    return render(request, 'accounts/LOGIN.html', {
        'register_form': form,
        'login_form': LoginForm()
    })

@login_required
def profile_view(request):
    """ویرایش پروفایل کاربر و نمایش اطلاعات اضافی"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('✅ پروفایل با موفقیت به‌روزرسانی شد!'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('⚠️ لطفاً خطاهای فرم را برطرف کنید.'))
    else:
        form = ProfileForm(instance=request.user)

    # محاسبه تعداد شغل‌ها
    business_count = request.user.send_businesses.count()

    # محاسبه تعداد کل بازدیدها
    total_views = request.user.send_businesses.aggregate(total_views=Sum('views'))['total_views'] or 0

    # محاسبه میانگین امتیاز
    avg_rating = request.user.send_businesses.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0

    context = {
        'form': form,
        'business_count': business_count,
        'total_views': total_views,
        'avg_rating': round(avg_rating, 1),
    }

    return render(request, 'accounts/PROFILE.html', context)

@login_required
def businesses_view(request):
    """نمایش لیست شغل‌های کاربر"""
    businesses = request.user.send_businesses.all()
    context = {
        'businesses': businesses,
    }
    return render(request, 'accounts/businesses.html', context)