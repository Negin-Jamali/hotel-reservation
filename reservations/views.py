
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, DiscountCodeForm
from .models import Reservation, DiscountCode
from hotels.models import Hotel



@login_required
def reservation_create(request):
    success_reservation = None

    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)

            reserved_count = Reservation.objects.filter(
                room_type=reservation.room_type,
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in__lt=reservation.check_out,
                check_out__gt=reservation.check_in
            ).count()

            if reserved_count >= reservation.room_type.total_rooms:
                form.add_error(None, 'در این تاریخ اتاق خالی وجود ندارد.')
            else:
                nights = (reservation.check_out - reservation.check_in).days
                total_price = nights * reservation.room_type.price_per_night

                code_text = form.cleaned_data.get('discount_code_text')

                if code_text:
                    try:
                        discount = DiscountCode.objects.get(
                            code=code_text,
                            hotel=reservation.room_type.hotel,
                            is_active=True
                        )

                        if discount.discount_type == 'percent':
                            total_price -= (
                                total_price * discount.discount_value / 100
                            )
                        else:
                            total_price -= discount.discount_value

                        total_price = max(total_price, 0)
                        reservation.discount_code = discount

                    except DiscountCode.DoesNotExist:
                        form.add_error(
                            'discount_code_text',
                            'کد تخفیف معتبر نیست.'
                        )

                if form.is_valid():
                    reservation.customer = request.user
                    reservation.total_price = total_price
                    reservation.save()
                    success_reservation = reservation

    else:
        form = ReservationForm()

    return render(
        request,
        'reservations/reservation_form.html',
        {
            'form': form,
            'success_reservation': success_reservation,
        }
    )


@login_required
def discount_code_create(request, hotel_id):
    if request.user.role != 'hotel_manager':
        return redirect('hotels:hotel_list')

    hotel = get_object_or_404(
        Hotel,
        id=hotel_id,
        manager=request.user
    )

    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)

        if form.is_valid():
            discount = form.save(commit=False)
            discount.hotel = hotel
            discount.save()

            return redirect('accounts:manager_dashboard')

    else:
        form = DiscountCodeForm()

    return render(
        request,
        'reservations/discount_code_form.html',
        {
            'form': form,
            'hotel': hotel,
        }
    )
