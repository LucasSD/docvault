from django.contrib.auth import views as auth_views
from django.urls import path
from docvault.landing.views import register

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="landing/home.html")),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="landing/home.html"),
        name="logout",
    ),
    path(
        "accounts/password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="landing/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="landing/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="landing/password_reset_form.html",
            subject_template_name="landing/password_reset_subject.txt",
            email_template_name="landing/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="landing/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="landing/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="landing/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register/", register, name="register"),
]
