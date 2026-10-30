from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountCode(models.Model):
    DISCOUNT_TYPE = (
        ('percent', 'درصدی'),
        ('amount', 'مبلغ ثابت'),
    )
    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='discount_codes',
        verbose_name='هتل',
    )
    code = models.CharField(max_length=50, unique=True, verbose_name='کد تخفیف')
    discount_type = models.CharField(
        max_length=10, choices=DISCOUNT_TYPE,
        verbose_name='نوع تخفیف',
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name='مقدار تخفیف',
    )
    valid_from = models.DateTimeField(verbose_name='از تاریخ')
    valid_to = models.DateTimeField(verbose_name='تا تاریخ')
    max_uses = models.PositiveIntegerField(
        default=1, verbose_name='حداکثر تعداد استفاده',
    )
    used_count = models.PositiveIntegerField(
        default=0, verbose_name='تعداد استفاده شده',
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return self.code


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار تأیید'),
        ('confirmed', 'تأیید شده'),
        ('checked_in', 'ورود انجام شده'),
        ('checked_out', 'خروج انجام شده'),
        ('cancelled', 'لغو شده'),
    )

    customer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='مشتری',
    )
    room_type = models.ForeignKey(
        'hotels.RoomType',
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='نوع اتاق',
    )
    check_in = models.DateField(verbose_name='تاریخ ورود')
    check_out = models.DateField(verbose_name='تاریخ خروج')
    guests_count = models.PositiveSmallIntegerField(
        default=1, verbose_name='تعداد مهمان',
    )
    total_price = models.DecimalField(
        max_digits=12, decimal_places=0,
        verbose_name='قیمت کل',
    )
    discount_code = models.ForeignKey(
        DiscountCode,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reservations',
        verbose_name='کد تخفیف',
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='وضعیت',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.username} - {self.room_type} ({self.check_in} تا {self.check_out})"

    def nights_count(self):
        return (self.check_out - self.check_in).days


class Review(models.Model):
    customer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='مشتری',
    )
    hotel = models.ForeignKey(
        'hotels.Hotel',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='هتل',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز',
    )
    comment = models.TextField(blank=True, verbose_name='نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        unique_together = ('customer', 'hotel')

    def __str__(self):
        return f"{self.customer.username} - {self.hotel.name} ({self.rating}⭐)"