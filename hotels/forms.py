from django import forms
from .models import Hotel, RoomType


class HotelSearchForm(forms.Form):
    city = forms.CharField(
        label='شهر',
        required=False
    )

    check_in = forms.DateField(
        label='تاریخ ورود',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    check_out = forms.DateField(
        label='تاریخ خروج',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    guests_count = forms.IntegerField(
        label='تعداد مهمان',
        min_value=1,
        initial=1
    )

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError(
                'تاریخ خروج باید بعد از تاریخ ورود باشد.'
            )

        return cleaned_data


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name',
            'city',
            'address',
            'description',
            'star_rating',
            'latitude',
            'longitude',
        ]


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = [
            'title',
            'capacity',
            'price_per_night',
            'total_rooms',
            'amenities',
            'description',
        ]