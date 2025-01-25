from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        registration_form = CreateUserForm(request.POST)
        registration_form.instance.is_active = False

        if registration_form.is_valid():
            registration_form.save()

            return redirect("index")
        else:
            form = registration_form

    context = {"form": form}

    return render(request, "registration/register.html", context=context)
    

def email_verification(request):
    pass


def email_verification_sent(request):
    pass


def email_verification_success(request):
    pass


def email_verification_fail(request):
    pass
