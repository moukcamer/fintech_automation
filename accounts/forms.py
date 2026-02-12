from django import forms
from django.contrib.auth import authenticate
from .models import User


# ---------------- REGISTER ----------------

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['email', 'full_name']

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")

        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


# ---------------- LOGIN ----------------

class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Email ou mot de passe incorrect")
            self.user = user
        return cleaned

    def get_user(self):

        return self.user

