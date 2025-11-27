from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("details/", views.account_detail, name="account_detail"),
    path("edit/", views.edit_account, name="edit_account"),
    path("logout/", LogoutView.as_view(next_page=''), name="logout"),
    path("delete/", views.delete_account, name="delete_account"),
    
    path("password_change/", 
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"),
         name="password_change"),
         
    path("password_change/done/",
         auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
         name="password_change_done"),         

    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
        name="password_reset"),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done"),

    path(
        "reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name="password_reset_confirm"),

    path(
        "reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete"),     
]
