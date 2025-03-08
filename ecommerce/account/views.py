from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, UpdateUserForm, ForgotPasswordUserForm, PasswordResetUserForm
from payment.forms import ShippingForm
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserEmails, PasswordResetEmails
from payment.models import ShippingAddress, Order, OrderItem
from time import sleep


def _send_password_reset_email(request, email):

    try:
        user_found = get_object_or_404(User, email=email, is_active=True, is_staff=False, is_superuser=False)
    except Exception as exc:
        sleep(1)
        return

    try:
        password_reset_records = PasswordResetEmails.objects.filter(email=user_found.email, reset=False, user_id=user_found.pk).order_by("-date_sent")
        if password_reset_records:
            for record in password_reset_records:
                record.valid = False
                record.save()
    except Exception as exc:
        pass

    new_record = PasswordResetEmails()
    new_record.user = user_found
    new_record.email = email
    new_record.reset = False
    new_record.save()
    
    subject = "Password reset email"
    context = {
        "user": user_found,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user_found.pk)),
        "uemail": urlsafe_base64_encode(force_bytes(email)),
        "token": user_tokenizer.make_token(user_found)
    }
    message = render_to_string("password_reset/password_reset_message.html", context=context)

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[email],
        fail_silently=True,
    )


def _send_verification_email(request, user, email, *, registration_verification=False):

    new_record = UserEmails()
    new_record.user = user
    new_record.email = email
    new_record.verified = False
    new_record.registration_verification = registration_verification
    new_record.save()
    
    subject = "Account verification email"
    context = {
        "user": user,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "uemail": urlsafe_base64_encode(force_bytes(email)),
        "token": user_tokenizer.make_token(user)
    }
    message = render_to_string("registration/email_verification_message.html", context=context)

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[email],
        fail_silently=True,
    )


@user_passes_test(lambda user: not user.is_authenticated, login_url="dashboard")
def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        registration_form = CreateUserForm(request.POST)
        registration_form.instance.is_active = False

        if registration_form.is_valid():
            user = registration_form.save()

            _send_verification_email(request, user, user.email, registration_verification=True)

            messages.add_message(request, messages.SUCCESS, "Registered successfully")

            return render(request, "registration/email_verification.html", context={"result": "sent"})
        else:
            messages.add_message(request, messages.ERROR, "Couldn't register the user")
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
        user_found = get_object_or_404(User, pk=uid, email=uemail, is_active=False, is_staff=False, is_superuser=False)
    except Exception as exc:
        try:
            user_found = get_object_or_404(User, pk=uid, is_active=True, is_staff=False, is_superuser=False)
            user_email_record = UserEmails.objects.filter(email=uemail, verified=False, user_id=user_found.pk)

            if not user_email_record:
                return render(request, "registration/email_verification.html", context={"result": "fail"})    
        except Exception as exc:
            return render(request, "registration/email_verification.html", context={"result": "fail"})

    if user_found and user_tokenizer.check_token(user=user_found, token=token):
        try:
            not_unique_email_check = User.objects.filter(email=uemail, is_active=True, is_staff=False, is_superuser=False)

            if not_unique_email_check:
                return render(request, "registration/email_verification.html", context={"result": "fail"})

            user_email_record = UserEmails.objects.filter(email=uemail, verified=False, user_id=user_found.pk).order_by("-date_sent")[:1].get()

            if user_email_record:
                user_email_record.verified = True
                user_email_record.save()

                user_found.email = uemail

                if user_email_record.registration_verification:
                    user_found.is_active = True

                user_found.save()

        except Exception as exc:
            return render(request, "registration/email_verification.html", context={"result": "fail"})

        return render(request, "registration/email_verification.html", context={"result": "success"})
    else:
        return render(request, "registration/email_verification.html", context={"result": "fail"})


@user_passes_test(lambda user: not user.is_authenticated, login_url="dashboard")
def login(request):
    form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():
            
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user and user.is_active and not user.is_staff and not user.is_superuser:
                auth.login(request, user)

                messages.add_message(request, messages.SUCCESS, "Logged in successfully")

                return redirect("dashboard")
        
        messages.add_message(request, messages.ERROR, "Couldn't authenticate the user")


    context = {"form": form}

    return render(request, "login.html", context=context)


@user_passes_test(lambda user: user.is_active and not user.is_staff and not user.is_superuser, login_url="login")
@login_required(login_url="login")
def logout(request):

    temp_session_details = request.session.get("session_details")
    auth.logout(request)
    request.session["session_details"] = temp_session_details

    messages.add_message(request, messages.SUCCESS, "Logged out successfully")

    return redirect("index")


@user_passes_test(lambda user: user.is_active and not user.is_staff and not user.is_superuser, login_url="login")
@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html")


@user_passes_test(lambda user: user.is_active and not user.is_staff and not user.is_superuser, login_url="login")
@login_required(login_url="login")
def profile_management(request):

    current_user = User.objects.get(username=request.user)
    existing_email = current_user.email
    
    if request.method == "POST":
        update_form_email = UpdateUserForm(request.POST, instance=current_user)

        if update_form_email.is_valid():

            if "email" in update_form_email.changed_data:
                new_email = current_user.email

                current_user.email = existing_email
                current_user.save()

                _send_verification_email(request, current_user, new_email)

                return render(request, "registration/email_verification.html", context={"result": "sent"})
            
            elif update_form_email.changed_data:
                current_user.save()

            messages.add_message(request, messages.SUCCESS, "User data updated successfully")

        else:
            messages.add_message(request, messages.ERROR, "Couldn't update the user")

    form = UpdateUserForm(instance=current_user)
    context = {"form": form}

    return render(request, "profile_management.html", context=context)


@user_passes_test(lambda user: user.is_active and not user.is_staff and not user.is_superuser, login_url="login")
@login_required(login_url="login")
def delete_account(request):

    try:
        current_user = User.objects.get(username=request.user)
        current_user.is_active = False
        current_user.save()

        messages.add_message(request, messages.SUCCESS, "User has been deleted successfully")

        return render(request, "delete_account.html", context={"result": "success"})
    except Exception as exc:
        return render(request, "delete_account.html", context={"result": "fail"})


@user_passes_test(lambda user: not user.is_authenticated, login_url="dashboard")
def forgot_your_password(request):

    forgot_your_password_form = ForgotPasswordUserForm()
    
    if request.method == "POST":
        forgot_your_password_form = ForgotPasswordUserForm(request.POST)

        if forgot_your_password_form.is_valid():

            email = forgot_your_password_form.cleaned_data.get("email")

            _send_password_reset_email(request, email)
            
            return render(request, "password_reset/password_reset.html", context={"result": "sent"})

        else:
            messages.add_message(request, messages.ERROR, "Invalid email has been entered")

    form = forgot_your_password_form
    context = {"form": form}

    return render(request, "password_reset/forgot_your_password.html", context=context)


@user_passes_test(lambda user: not user.is_authenticated, login_url="dashboard")
def password_change(request, uidb64, uemailb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        uemail = force_str(urlsafe_base64_decode(uemailb64))
    except Exception as exc:
        return render(request, "password_reset/password_reset.html", context={"result": "fail"})

    try:
        user_found = get_object_or_404(User, pk=uid, email=uemail, is_active=True, is_staff=False, is_superuser=False)
        password_reset_record = PasswordResetEmails.objects.filter(email=user_found.email, reset=False, valid=True, user_id=user_found.pk).order_by("-date_sent")[:1].get()
    except Exception as exc:
        return render(request, "password_reset/password_reset.html", context={"result": "fail"})

    valid_token = user_tokenizer.check_token(user=user_found, token=token)
    if not valid_token:
        return render(request, "password_reset/password_reset.html", context={"result": "fail"})

    password_reset_form = PasswordResetUserForm(user_found)

    if user_found and password_reset_record and valid_token:

        if request.method == "POST":
            password_reset_form = PasswordResetUserForm(user_found, request.POST)

            if password_reset_form.is_valid():
                try:
                    password_reset_form.save()

                    password_reset_record.reset = True
                    password_reset_record.valid = False
                    password_reset_record.save()

                except Exception as exc:
                    return render(request, "password_reset/password_reset.html", context={"result": "fail"})

                return render(request, "password_reset/password_reset.html", context={"result": "success"})                

            else:
                messages.add_message(request, messages.ERROR, "Password cannot be reset")

    form = password_reset_form
    context = {"form": form}

    return render(request, "password_reset/password_reset_passwords.html", context=context)



@user_passes_test(lambda user: user.is_active and not user.is_staff and not user.is_superuser, login_url="login")
@login_required(login_url="login")
def manage_shipping(request):

    try:
        shipping_address = ShippingAddress.objects.filter(user=request.user.id).order_by("-date_created")[:1].get()
    except Exception as exc:
        shipping_address = None

    shipping_address_form = ShippingForm(instance=shipping_address)

    if request.method == "POST":
        shipping_address_form = ShippingForm(request.POST, instance=shipping_address)

        if shipping_address_form.is_valid():

            shipping_address_form.instance.user = request.user
            shipping_address_form.save()
            
            return redirect("dashboard")

        else:
            messages.add_message(request, messages.ERROR, "Unable to update shipping address")

    form = shipping_address_form
    context = {"form": form}

    return render(request, "manage_shipping.html", context=context)


@user_passes_test(lambda user: user.is_active and not user.is_staff and not user.is_superuser, login_url="login")
@login_required(login_url="login")
def track_orders(request):

    context = {}

    try:
        orders = Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.filter(order__in=orders).select_related("product")

        context = {"orders": orders, "order_items": order_items}
    except Exception as exc:
        pass

    return render(request, "track_orders.html", context=context)
