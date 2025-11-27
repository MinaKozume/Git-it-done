from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

    # Override save method to split full name
    def save(self, commit=True):
        user = super().save(commit=False)
        name = self.cleaned_data.get("full_name").split(" ", 1)

        user.first_name = name[0]
        if len(name) > 1:
            user.last_name = name[1]

        if commit:
            user.save()
        return user


class EditAccountForm(forms.ModelForm):
    full_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        name = self.cleaned_data.get("full_name").split(" ", 1)

        user.first_name = name[0]
        if len(name) > 1:
            user.last_name = name[1]

        if commit:
            user.save()
        return user
