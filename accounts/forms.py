from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not email:
            raise forms.ValidationError("Email is required.")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already used.")

        return email