from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("category/<str:cat>/", views.show_category, name="show_category"),
    path("brand/<str:brand>/", views.show_brand, name="show_brand"),
    path("details/<slug:product>/", views.show_details, name="show_details"),
]
