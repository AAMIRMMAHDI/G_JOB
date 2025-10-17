from django.db import models

class AboutPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان صفحه")
    subtitle = models.CharField(max_length=500, verbose_name="زیرعنوان صفحه")
    description = models.TextField(verbose_name="توضیحات")
    stat_store_icon = models.CharField(max_length=100, default="store", verbose_name="آیکون فروشگاه")
    stat_store_number = models.CharField(max_length=50, default="۱,۲۵۰+", verbose_name="تعداد فروشگاه")
    stat_store_label = models.CharField(max_length=100, default="فروشگاه فعال", verbose_name="برچسب فروشگاه")
    stat_users_icon = models.CharField(max_length=100, default="users", verbose_name="آیکون کاربران")
    stat_users_number = models.CharField(max_length=50, default="۵۰,۰۰۰+", verbose_name="تعداد کاربران")
    stat_users_label = models.CharField(max_length=100, default="کاربر ثبت‌نام شده", verbose_name="برچسب کاربران")
    stat_rating_icon = models.CharField(max_length=100, default="star", verbose_name="آیکون رضایت")
    stat_rating_number = models.CharField(max_length=50, default="۴.۸/۵", verbose_name="امتیاز رضایت")
    stat_rating_label = models.CharField(max_length=100, default="رضایت کاربران", verbose_name="برچسب رضایت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "صفحه درباره ما"
        verbose_name_plural = "About Us Pages"

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    role = models.CharField(max_length=200, verbose_name="نقش")
    bio = models.TextField(verbose_name="بیوگرافی")
    image = models.ImageField(upload_to='team_images/', verbose_name="تصویر")
    linkedin_url = models.URLField(blank=True, verbose_name="لینکدین")
    twitter_url = models.URLField(blank=True, verbose_name="توییتر")
    github_url = models.URLField(blank=True, verbose_name="گیت‌هاب")
    instagram_url = models.URLField(blank=True, verbose_name="اینستاگرام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "Team members"

    def __str__(self):
        return self.name




from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"





from django.db import models

class ContactInfo(models.Model):
    title = models.CharField(max_length=100, default="با ما در ارتباط باشید")
    description = models.TextField(default="تیم پشتیبانی ما آماده پاسخگویی به سوالات و دریافت پیشنهادات شما می‌باشد.")
    address = models.CharField(max_length=255, default="تهران، خیابان ولیعصر، پلاک ۱۲۳۴، طبقه ۵")
    phone = models.CharField(max_length=20, default="۰۲۱-۱۲۳۴۵۶۷۸")
    email = models.EmailField(default="info@example.com")
    work_hours = models.CharField(max_length=100, default="شنبه تا چهارشنبه: ۸:۰۰ - ۱۷:۰۰ | پنجشنبه: ۸:۰۰ - ۱۴:۰۰")

    def __str__(self):
        return "اطلاعات تماس سایت"










