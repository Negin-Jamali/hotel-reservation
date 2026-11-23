from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Hotel, RoomType
from .forms import HotelSearchForm, HotelForm, RoomTypeForm
from reservations.models import Reservation


def hotel_list(request):
    form = HotelSearchForm(request.GET or None)
    available_room_types = []

    if request.GET and form.is_valid():
        city = form.cleaned_data.get('city')
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')
        guests_count = form.cleaned_data.get('guests_count')

        room_types = RoomType.objects.select_related('hotel').filter(
            capacity__gte=guests_count
        )

        if city:
            room_types = room_types.filter(
                hotel__city__icontains=city
            )

        if check_in and check_out:
            for room_type in room_types:
                reserved_count = Reservation.objects.filter(
                    room_type=room_type,
                    status__in=['pending', 'confirmed', 'checked_in'],
                    check_in__lt=check_out,
                    check_out__gt=check_in
                ).count()

                available_count = room_type.total_rooms - reserved_count

                if available_count > 0:
                    available_room_types.append({
                        'room_type': room_type,
                        'available_count': available_count
                    })

    return render(
        request,
        'hotels/hotel_list.html',
        {
            'form': form,
            'available_room_types': available_room_types,
        }
    )


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room_types = RoomType.objects.filter(hotel=hotel)

    return render(
        request,
        'hotels/hotel_detail.html',
        {
            'hotel': hotel,
            'room_types': room_types,
        }
    )


@login_required
def hotel_create(request):
    if request.user.role != 'hotel_manager':
        return redirect('hotels:hotel_list')

    if request.method == 'POST':
        form = HotelForm(request.POST)

        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.manager = request.user
            hotel.save()

            return redirect('accounts:manager_dashboard')

    else:
        form = HotelForm()

    return render(
        request,
        'hotels/hotel_form.html',
        {'form': form}
    )


@login_required
def room_type_create(request, hotel_id):
    if request.user.role != 'hotel_manager':
        return redirect('hotels:hotel_list')

    hotel = get_object_or_404(
        Hotel,
        id=hotel_id,
        manager=request.user
    )

    if request.method == 'POST':
        form = RoomTypeForm(request.POST)

        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.hotel = hotel
            room_type.save()

            return redirect('accounts:manager_dashboard')

    else:
        form = RoomTypeForm()

    return render(
        request,
        'hotels/room_type_form.html',
        {
            'form': form,
            'hotel': hotel,
        }
    )
@login_required
def hotel_reservations(request):
    if request.user.role != 'hotel_manager':
        return redirect('hotels:hotel_list')

    reservations = Reservation.objects.filter(
        room_type__hotel__manager=request.user
    )

    return render(
        request,
        'hotels/hotel_reservations.html',
        {'reservations': reservations}
    )
@login_required
def room_status(request):
    if request.user.role != 'hotel_manager':
        return redirect('hotels:hotel_list')

    room_types = RoomType.objects.filter(
        hotel__manager=request.user
    )

    room_status_list = []

    for room_type in room_types:
        reserved_count = Reservation.objects.filter(
            room_type=room_type,
            status__in=['pending', 'confirmed', 'checked_in']
        ).count()

        available_count = room_type.total_rooms - reserved_count

        room_status_list.append({
            'room_type': room_type,
            'reserved_count': reserved_count,
            'available_count': available_count,
        })

    return render(
        request,
        'hotels/room_status.html',
        {'room_status_list': room_status_list}
    )