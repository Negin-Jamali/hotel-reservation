
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm


@login_required
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)

            reservation.customer = request.user

            nights = (
                reservation.check_out - reservation.check_in
            ).days

            reservation.total_price = (
                nights * reservation.room_type.price_per_night
            )

            reservation.save()

            return redirect('hotels:hotel_list')

    else:
        form = ReservationForm()

    return render(
        request,
        'reservations/reservation_form.html',
        {'form': form}
    )
