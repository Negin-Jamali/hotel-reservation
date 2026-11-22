
from django.shortcuts import render
from .models import Hotel
from .forms import HotelSearchForm


def hotel_list(request):
    hotels = Hotel.objects.all()
    form = HotelSearchForm(request.GET or None)

    return render(
        request,
        'hotels/hotel_list.html',
        {
            'hotels': hotels,
            'form': form,
        }
    )
