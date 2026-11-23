
from django import forms
from .models import Reservation, DiscountCode


class ReservationForm(forms.ModelForm):
    discount_code_text = forms.CharField(
        label='کد تخفیف',
        required=False
    )

    class Meta:
        model = Reservation
        fields = ['room_type', 'check_in', 'check_out', 'guests_count']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room_type = cleaned_data.get('room_type')
        guests_count = cleaned_data.get('guests_count')

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError(
                'تاریخ خروج باید بعد از تاریخ ورود باشد.'
            )

        if room_type and guests_count:
            if guests_count > room_type.capacity:
                raise forms.ValidationError(
                    'تعداد مهمان‌ها بیشتر از ظرفیت اتاق است.'
                )

        return cleaned_data


class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = [
            'code',
            'discount_type',
            'discount_value',
            'valid_from',
            'valid_to',
            'max_uses',
            'is_active',
        ]
