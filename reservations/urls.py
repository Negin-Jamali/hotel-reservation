
from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('create/', views.reservation_create, name='reservation_create'),
    path(
        'discount/create/<int:hotel_id>/',
        views.discount_code_create,
        name='discount_code_create'
    ),
]
