from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="landing/home.html")),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="landing/home.html"),
        name="logout",
    ),
    path(
        "accounts/password_change/",
        auth_views.PasswordChangeView.as_view(template_name="landing/password_change_form.html"),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="landing/password_change_done.html"),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(template_name="landing/password_reset_form.html"),
        name="password_reset",
    ),
]

