from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        registration_form = CreateUserForm(request.POST)
        registration_form.instance.is_active = False

        if registration_form.is_valid():
            user = registration_form.save()

            subject = "Account verification email"
            context = {
                "user": user,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "username": urlsafe_base64_encode(force_bytes(user.username)),
                "token": user_tokenizer.make_token(user)
            }
            message = render_to_string("registration/email_verification.html", context=context)

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )

            return redirect("email_verification_sent")
        else:
            form = registration_form

    context = {"form": form}

    return render(request, "registration/register.html", context=context)
    

def email_verification(request, uidb64, usernameb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    username = force_str(urlsafe_base64_decode(usernameb64))
    user = get_object_or_404(User, pk=uid, username=username, is_active=False, is_staff=False, is_superuser=False)

    if user and user_tokenizer.check_token(user=user, token=token):
        user.is_active = True
        user.save()
        return redirect("email_verification_success")
    else:
        return redirect("email_verification_fail")


def email_verification_sent(request):
    return render(request, "registration/email_verification_sent.html")


def email_verification_success(request):
    return render(request, "registration/email_verification_success.html")


def email_verification_fail(request):
    return render(request, "registration/email_verification_fail.html")
