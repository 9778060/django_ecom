from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("email_verification/<str:uidb64>/<str:uemailb64>/<str:token>/", views.email_verification, name="email_verification"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/profile", views.profile_management, name="profile_management"),
    path("dashboard/delete", views.delete_account, name="delete_account"),
    # path("forgot_your_password/", auth_views.PasswordResetView.as_view(), name="forgot_your_password"),
    path("forgot_your_password/", views.forgot_your_password, name="forgot_your_password"),
    # path("password_reset/<str:uidb64>/<str:uemailb64>/<str:token>/", views.password_reset, name="password_reset"),
    path("password_change/<str:uidb64>/<str:uemailb64>/<str:token>/", views.password_change, name="password_change"),
    path("logout/", views.logout, name="logout"),
]
