from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Count, Avg
from django.utils.text import slugify
from django.http import JsonResponse
from .forms import (
    BusinessRegisterForm,
    BusinessImageForm,
    ServiceForm,
    BusinessHoursForm,
    BusinessRatingForm,
    MessageForm,
)
from .models import Business, BusinessImage, Service, BusinessHours, Category, BusinessRating, Conversation, Message
import json

@login_required
def business_register_view(request):
    if request.method == 'POST':
        form = BusinessRegisterForm(request.POST)
        image_form = BusinessImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            # ذخیره خدمات
            services = request.POST.getlist('services')
            icons = request.POST.getlist('icons')
            for service_name, icon in zip(services, icons):
                if service_name:
                    Service.objects.create(business=business, name=service_name, icon=icon)

            # ذخیره ساعات کاری
            days_list = [
                ('شنبه - چهارشنبه', 'weekday'),
                ('پنجشنبه', 'thursday'),
                ('جمعه', 'friday'),
            ]
            for days, prefix in days_list:
                start_time = request.POST.get(f'{prefix}_start')
                end_time = request.POST.get(f'{prefix}_end')
                is_closed = request.POST.get(f'{prefix}_closed') == 'on'
                if not is_closed and start_time and end_time:
                    BusinessHours.objects.create(
                        business=business,
                        days=days,
                        start_time=start_time,
                        end_time=end_time,
                        is_closed=False
                    )
                else:
                    BusinessHours.objects.create(
                        business=business,
                        days=days,
                        is_closed=True
                    )

            # ذخیره تصاویر
            for file in files:
                BusinessImage.objects.create(business=business, image=file)

            messages.success(request, _('شغل با موفقیت ثبت شد! پس از تأیید نهایی نمایش داده خواهد شد.'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('لطفاً خطاهای فرم را برطرف کنید'))
    else:
        form = BusinessRegisterForm()
        image_form = BusinessImageForm()

    service_choices = [
        ('تحویل_در_محل', _('تحویل در محل'), 'fa-truck'),
        ('رزرو_آنلاین', _('رزرو آنلاین'), 'fa-calendar-check'),
        ('پارکینگ', _('پارکینگ'), 'fa-parking'),
        ('وای_فای_رایگان', _('وای‌فای رایگان'), 'fa-wifi'),
        ('فضای_خانوادگی', _('فضای خانوادگی'), 'fa-users'),
        ('پذیرش_کارت', _('پذیرش کارت'), 'fa-credit-card'),
    ]

    hours_choices = {
        'weekday': {'start': ['۸:۰۰', '۹:۰۰', '۱۰:۰۰'], 'end': ['۱۷:۰۰', '۱۸:۰۰', '۱۹:۰۰']},
        'thursday': {'start': ['۸:۰۰', '۹:۰۰'], 'end': ['۱۴:۰۰', '۱۵:۰۰']},
    }

    return render(request, 'send/SEND.html', {
        'form': form,
        'image_form': image_form,
        'service_choices': service_choices,
        'hours_choices': hours_choices,
    })

def business_list_view(request):
    categories = request.GET.getlist('category[]')
    cities = request.GET.getlist('city[]')
    search = request.GET.get('search')

    businesses = Business.objects.filter(is_approved=True).exclude(slug='')

    if categories and 'all' not in categories:
        businesses = businesses.filter(category__slug__in=categories)

    if cities and 'all' not in cities:
        businesses = businesses.filter(city__in=cities)

    if search:
        businesses = businesses.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )

    all_categories = Category.objects.annotate(
        count=Count('businesses', filter=Q(businesses__is_approved=True))
    )
    all_cities = Business.objects.filter(is_approved=True).values('city').annotate(
        count=Count('city')
    ).order_by('city')

    service_choices = [
        ('تحویل_در_محل', _('تحویل در محل'), 'fa-truck'),
        ('رزرو_آنلاین', _('رزرو آنلاین'), 'fa-calendar-check'),
        ('پارکینگ', _('پارکینگ'), 'fa-parking'),
        ('وای_فای_رایگان', _('وای‌فای رایگان'), 'fa-wifi'),
        ('فضای_خانوادگی', _('فضای خانوادگی'), 'fa-users'),
        ('پذیرش_کارت', _('پذیرش کارت'), 'fa-credit-card'),
    ]

    return render(request, 'send/LIST.html', {
        'businesses': businesses,
        'categories': all_categories,
        'cities': all_cities,
        'service_choices': service_choices,
        'current_categories': categories if categories else ['all'],
        'current_cities': cities if cities else ['all'],
        'current_search': search or '',
    })

def business_detail_view(request, slug):
    business = get_object_or_404(Business, slug=slug, is_approved=True)
    avg_rating = business.ratings.aggregate(Avg('rating'))['rating__avg'] or 0.0
    rating_count = business.ratings.count()

    rating_percentages = {}
    for i in range(1, 6):
        count = business.ratings.filter(rating__gte=i - 0.5, rating__lt=i + 0.5).count()
        percentage = (count / rating_count * 100) if rating_count > 0 else 0
        rating_percentages[str(i)] = round(percentage, 1)

    similar_businesses = Business.objects.filter(
        category=business.category,
        is_approved=True
    ).exclude(slug=slug).exclude(slug='')[:3]

    for similar in similar_businesses:
        similar.avg_rating = similar.ratings.aggregate(avg=Avg('rating'))['avg'] or 0

    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = BusinessRating.objects.filter(
            business=business, 
            user=request.user
        ).exists()

    return render(request, 'send/DETAIL.html', {
        'business': business,
        'images': business.images.all(),
        'services': business.services.all(),
        'hours': business.hours.all(),
        'avg_rating': avg_rating,
        'rating_count': rating_count,
        'ratings': business.ratings.all().order_by('-created_at')[:3],
        'rating_percentages': rating_percentages,
        'similar_businesses': similar_businesses,
        'user_has_reviewed': user_has_reviewed,
    })

@login_required
def add_review_view(request, slug):
    business = get_object_or_404(Business, slug=slug, is_approved=True)
    existing_review = BusinessRating.objects.filter(business=business, user=request.user).first()
    if existing_review:
        messages.warning(request, _('شما قبلاً برای این کسب‌وکار نظر داده‌اید.'))
        return redirect('send:business_detail', slug=slug)

    if request.method == 'POST':
        form = BusinessRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.business = business
            rating.user = request.user
            rating.save()
            messages.success(request, _('نظر شما با موفقیت ثبت شد!'))
            return redirect('send:business_detail', slug=slug)
        else:
            messages.error(request, _('لطفاً خطاهای فرم را برطرف کنید'))
    else:
        form = BusinessRatingForm()

    return render(request, 'send/COMANT.html', {
        'form': form,
        'business': business,
    })

@login_required
def chat_view(request, slug=None):
    is_owner = False
    selected_conversation = None
    messages = []
    business = None

    if slug:
        # User is accessing chat from a specific business post
        business = get_object_or_404(Business, slug=slug, is_approved=True)
        conversation, created = Conversation.objects.get_or_create(
            business=business,
            user=request.user
        )
        selected_conversation = conversation
        messages = conversation.messages.all().select_related('sender')
    else:
        # Check if user is an owner
        owned_businesses = Business.objects.filter(owner=request.user, is_approved=True)
        if owned_businesses.exists():
            is_owner = True
            if request.GET.get('conversation_id'):
                selected_conversation = get_object_or_404(
                    Conversation, 
                    id=request.GET.get('conversation_id'), 
                    business__owner=request.user
                )
                messages = selected_conversation.messages.all().select_related('sender')

    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            if conversation.user != request.user and conversation.business.owner != request.user:
                return JsonResponse({'status': 'error', 'message': 'Access denied'}, status=403)
        else:
            conversation = selected_conversation

        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            if message.file:
                file_type = message.file.content_type.split('/')[0]
                message.file_type = file_type if file_type in ['image', 'video', 'application'] else 'file'
            message.save()
            return JsonResponse({
                'status': 'success',
                'message': {
                    'content': message.content,
                    'file_url': message.file.url if message.file else None,
                    'file_type': message.file_type,
                    'sender': message.sender.username,
                    'business_name': message.conversation.business.name,
                    'business_slug': message.conversation.business.slug,
                    'created_at': message.created_at.strftime('%H:%M'),
                    'is_sent': message.sender == request.user
                }
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

    # Load conversations based on user role
    if is_owner:
        conversations = Conversation.objects.filter(business__in=owned_businesses).select_related('business', 'user')
    else:
        conversations = Conversation.objects.filter(user=request.user).select_related('business')

    return render(request, 'send/chat.html', {
        'business': business,
        'is_owner': is_owner,
        'selected_conversation': selected_conversation,
        'messages': messages,
        'form': MessageForm(),
        'conversations': conversations
    })

@login_required
def get_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if conversation.user != request.user and conversation.business.owner != request.user:
        return JsonResponse({'status': 'error', 'message': 'Access denied'}, status=403)
    messages = conversation.messages.all().select_related('sender')
    
    messages_data = [
        {
            'content': msg.content,
            'file_url': msg.file.url if msg.file else None,
            'file_type': msg.file_type,
            'sender': msg.sender.username,
            'business_name': msg.conversation.business.name,
            'business_slug': msg.conversation.business.slug,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_sent': msg.sender == request.user
        }
        for msg in messages
    ]
    
    return JsonResponse({
        'status': 'success',
        'messages': messages_data
    })