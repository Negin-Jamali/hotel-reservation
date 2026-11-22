
from django import forms


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
