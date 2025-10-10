from django.shortcuts import render
from .models import AboutPage, TeamMember

def about_view(request):
    # گرفتن اولین رکورد صفحه درباره ما
    about_page = AboutPage.objects.first()
    
    # گرفتن همه اعضای تیم
    team_members = TeamMember.objects.all()

    # آماده‌سازی داده‌ها برای قالب
    context = {
        'about_page': about_page,
        'team_members': [
            {
                'name': member.name,
                'role': member.role,
                'bio': member.bio,
                'image': member.image.url if member.image else None,
                'social': [
                    {'platform': 'linkedin', 'url': member.linkedin_url} if member.linkedin_url else None,
                    {'platform': 'twitter', 'url': member.twitter_url} if member.twitter_url else None,
                    {'platform': 'github', 'url': member.github_url} if member.github_url else None,
                    {'platform': 'instagram', 'url': member.instagram_url} if member.instagram_url else None,
                ]
            } for member in team_members
        ],
        'stats': []
    }

    # اضافه کردن آمار فقط اگر about_page موجود باشد
    if about_page:
        context['stats'] = [
            {
                'icon': about_page.stat_store_icon,
                'number': about_page.stat_store_number,
                'label': about_page.stat_store_label
            },
            {
                'icon': about_page.stat_users_icon,
                'number': about_page.stat_users_number,
                'label': about_page.stat_users_label
            },
            {
                'icon': about_page.stat_rating_icon,
                'number': about_page.stat_rating_number,
                'label': about_page.stat_rating_label
            },
        ]

    return render(request, 'root/about.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm
from .models import ContactInfo

def contact_view(request):
    # فرم تماس
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد!")
            return redirect('root:contact')
    else:
        form = ContactMessageForm()

    # اطلاعات تماس
    contact_info = ContactInfo.objects.first()  # فقط اولین رکورد

    return render(request, 'root/contact.html', {'form': form, 'contact_info': contact_info})
