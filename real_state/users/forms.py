from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "name",
            "last_name",
            "company_name",
        )

    def save(self, commit=True):
        user = User.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            name=self.cleaned_data["name"],
            last_name=self.cleaned_data["last_name"],
            company_name=self.cleaned_data["company_name"],
        )
        return user
