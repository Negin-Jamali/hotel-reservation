from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='hotels',
        verbose_name='مدیر هتل',
    )
    name = models.CharField(max_length=200, verbose_name='نام هتل')
    city = models.CharField(max_length=100, verbose_name='شهر')
    address = models.TextField(verbose_name='آدرس')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    star_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='تعداد ستاره',
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        verbose_name='عرض جغرافیایی',
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        verbose_name='طول جغرافیایی',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'هتل'
        verbose_name_plural = 'هتل‌ها'

    def __str__(self):
        return f"{self.name} - {self.city}"


class RoomType(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='room_types',
        verbose_name='هتل',
    )
    title = models.CharField(max_length=100, verbose_name='عنوان اتاق')
    capacity = models.PositiveSmallIntegerField(verbose_name='ظرفیت')
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name='قیمت هر شب (تومان)',
    )
    total_rooms = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='تعداد اتاق از این نوع',
    )
    amenities = models.TextField(
        blank=True,
        verbose_name='امکانات',
        help_text='امکانات را با کاما جدا کنید',
    )
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'نوع اتاق'
        verbose_name_plural = 'انواع اتاق'

    def __str__(self):
        return f"{self.hotel.name} - {self.title}"