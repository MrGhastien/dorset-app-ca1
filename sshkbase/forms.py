from django.contrib.auth.forms import PasswordResetForm
from django import forms


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'user-box',
        'placeholder': 'example@gaming.mlg',
        'type': 'email',
        'name': 'email'
    }))
