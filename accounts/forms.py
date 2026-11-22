
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='ایمیل'
    )

    phone = forms.CharField(
        required=False,
        label='شماره تماس'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'

        if commit:
            user.save()

        return user
