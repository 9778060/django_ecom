from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import Http404


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
                "uemail": urlsafe_base64_encode(force_bytes(user.email)),
                "token": user_tokenizer.make_token(user)
            }
            message = render_to_string("registration/email_verification_message.html", context=context)

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )

            return render(request, "registration/email_verification.html", context={"result": "sent"})
        else:
            form = registration_form

    context = {"form": form}

    return render(request, "registration/register.html", context=context)
    

def email_verification(request, uidb64, uemailb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        uemail = force_str(urlsafe_base64_decode(uemailb64))
    except Exception as exc:
        return render(request, "registration/email_verification.html", context={"result": "fail"})
    
    try:
        user = get_object_or_404(User, pk=uid, email=uemail, is_active=False, is_staff=False, is_superuser=False)
    except Exception as exc:
        return render(request, "registration/email_verification.html", context={"result": "fail"})

    if user and user_tokenizer.check_token(user=user, token=token):
        user.is_active = True
        user.save()
        return render(request, "registration/email_verification.html", context={"result": "success"})
    else:
        return render(request, "registration/email_verification.html", context={"result": "fail"})

