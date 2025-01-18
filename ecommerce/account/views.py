from django.shortcuts import render, redirect
from .forms import CreateUserForm


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        registration_form = CreateUserForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            
            return redirect("index")
        else:
            form = registration_form

    context = {"form": form}

    return render(request, "registration/register.html", context=context)
    