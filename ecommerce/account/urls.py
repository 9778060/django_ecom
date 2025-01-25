from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("email_verification/<str:uidb64>/<str:usernameb64>/<str:token>/", views.email_verification, name="email_verification"),
    path("email_verification_sent/", views.email_verification_sent, name="email_verification_sent"),
    path("email_verification_success/", views.email_verification_success, name="email_verification_success"),
    path("email_verification_fail/", views.email_verification_fail, name="email_verification_fail"),
    path("login/", views.register, name="login"),
]
