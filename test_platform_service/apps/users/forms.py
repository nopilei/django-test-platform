from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from .models import TestUser
from django import forms
from django.forms import ModelForm


class TestSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
    }


class TestLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TestRegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if TestUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=False):
        user = super().save(commit=commit)
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = TestUser
        fields = ("username", "email", "password1", "password2")


class TestUserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget = forms.FileInput()

    class Meta:
        fields = ['photo', 'first_name', 'last_name', 'date_of_birth', 'description', ]
        model = TestUser



