from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def not_found_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        # کاربر لاگین کرده → صفحه 13.html
        return render(request, '404.html', status=200)  # یا 404 اگر می‌خوای کد وضعیت 404 باشه
    else:
        # کاربر لاگین نکرده → صفحه 404.html
        return render(request, 'accounts/LOGIN.html', status=404)