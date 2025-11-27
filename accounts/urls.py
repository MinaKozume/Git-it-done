from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("details/", views.account_detail, name="account_detail"),
    path("edit/", views.edit_account, name="edit_account"),
    path("password_change/", 
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"),
         name="password_change"),
         
    path("password_change/done/",
         auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
         name="password_change_done"),         

    path("delete/", views.delete_account, name="delete_account"),
]
