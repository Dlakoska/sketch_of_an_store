from catalog.forms import StyleFormMixin
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm, PasswordChangeForm
from django import forms
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')