from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_staff = False
        self.is_superuser = False
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True


    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is not unique")

        return email
