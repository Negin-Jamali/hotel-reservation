from django.contrib import admin
from .models import DiscountCode, Reservation, Review


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'hotel', 'discount_type', 'discount_value', 'is_active')
    list_filter = ('discount_type', 'is_active')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'room_type', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in')
    search_fields = ('customer__username', 'room_type__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'hotel', 'rating', 'created_at')
    list_filter = ('rating',)