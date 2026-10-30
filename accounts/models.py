from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('hotel_manager', 'مدیر هتل'),
        ('customer', 'مشتری'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
        verbose_name='نقش',
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name='شماره تماس')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def is_hotel_manager(self):
        return self.role == 'hotel_manager'

    def is_customer(self):
        return self.role == 'customer'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"