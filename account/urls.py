from django.urls import path
from django.contrib.auth import views as auth_views

from account.views import (
    signup_view,
    login_view,
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
)

app_name = "accounts"

urlpatterns = [
    # Auth
    path("signup", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Password reset
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
