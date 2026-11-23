from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('create/', views.hotel_create, name='hotel_create'),
    path(
        'hotel/<int:hotel_id>/room/create/',
        views.room_type_create,
        name='room_type_create'
    ),
    path(
        'manager/reservations/',
        views.hotel_reservations,
        name='hotel_reservations'
    ),
    path(
        'manager/room-status/',
        views.room_status,
        name='room_status'
    ),
]