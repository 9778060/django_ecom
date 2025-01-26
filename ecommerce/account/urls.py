from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("email_verification/<str:uidb64>/<str:uemailb64>/<str:token>/", views.email_verification, name="email_verification"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="logout"),
]
