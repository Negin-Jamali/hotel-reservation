
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

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        label='نقش کاربری'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'role',
            'password1',
            'password2',
        ]
