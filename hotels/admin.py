from django.contrib import admin
from .models import Hotel, RoomType


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating', 'manager')
    list_filter = ('city', 'star_rating')
    search_fields = ('name', 'city')


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'capacity', 'price_per_night', 'total_rooms')
    list_filter = ('hotel',)
    search_fields = ('title', 'hotel__name')