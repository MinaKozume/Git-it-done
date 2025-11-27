from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    # Login/Signup/Account
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("details/", views.account_detail, name="account_detail"),
    path("edit/", views.edit_account, name="edit_account"),
    path("logout/", LogoutView.as_view(next_page='accounts:login'), name="logout"),
    path("delete/", views.delete_account, name="delete_account"),

    # Password change
    path("password_change/", views.change_password, name="password_change"),
    path("password_change/done/", views.CustomPasswordChangeDoneView.as_view(), name="password_change_done"),

    # Password reset (web page + email template)
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",           # Web page where user enters email
            email_template_name="accounts/password_reset_email.html",  # Separate email template
            subject_template_name="accounts/password_reset_subject.txt", # Email subject
            success_url="/accounts/password_reset/done/",              # Redirect after submitting email
        ),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    # Password reset confirm (link from email)
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/accounts/reset/done/"
        ),
        name="password_reset_confirm"
    ),

    # Password reset complete
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
