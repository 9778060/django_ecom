from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
   
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True


    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is not unique")

        return email


class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["email"]
        exclude = ["username", "password"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email, pk=self.instance.pk).exists():
            raise forms.ValidationError("Cannot update the same details")

        return email
    

class ForgotPasswordUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["email"]
        exclude = ["username", "password"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


class PasswordResetUserForm(SetPasswordForm):
   
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
        exclude = ["username", "email"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].required = True
        self.fields["new_password2"].required = True
