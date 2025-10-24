from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView

app_name = 'accounts'

urlpatterns = [
    # مسیر ورود
    path('login/', views.login_view, name='login'),
    # مسیر ثبت‌نام
    path('register/', views.register_view, name='register'),
    # مسیر پروفایل
    path('profile/', views.profile_view, name='profile'),
    # مسیر نمایش شغل‌ها
    path('businesses/', views.businesses_view, name='businesses'),
    # مسیر خروج با استفاده از LogoutView
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    # مسیر بازنشانی رمز عبور
    path('password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    # مسیر تکمیل درخواست بازنشانی رمز عبور
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    # مسیر تأیید بازنشانی رمز عبور
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    # مسیر تکمیل بازنشانی رمز عبور
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]