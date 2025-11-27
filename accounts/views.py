from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import SignupForm, EditAccountForm

from django.contrib.auth.views import PasswordChangeDoneView


# -------------------------
# SIGN UP
# -------------------------
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:account_detail')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You may now log in.")
            return redirect("accounts:login")
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {"form": form})


# -------------------------
# LOGIN
# -------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:account_detail')

    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # Login using email OR username
        try:
            user = User.objects.get(email=username_or_email)
            username = user.username
        except User.DoesNotExist:
            username = username_or_email  # user may have entered username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("accounts:account_detail")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'accounts/login.html')


# -------------------------
# ACCOUNT DETAIL PAGE
# -------------------------
@login_required
def account_detail(request):
    return render(request, 'accounts/account_detail.html')


# -------------------------
# EDIT ACCOUNT
# -------------------------
@login_required
def edit_account(request):
    if request.method == "POST":
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully.")
            return redirect("accounts:account_detail")
    else:
        # Pre-fill full_name field
        full_name = f"{request.user.first_name} {request.user.last_name}"
        form = EditAccountForm(instance=request.user, initial={"full_name": full_name})

    return render(request, 'accounts/edit_account.html', {"form": form})


# -------------------------
# CHANGE PASSWORD
# -------------------------
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, "Password changed successfully.")
            return redirect("accounts:password_change_done")  # Redirect to the custom done page
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {"form": form})


# -------------------------
# DELETE ACCOUNT
# -------------------------
@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password")

        if request.user.check_password(password):
            request.user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect("homepage:homepage")
        else:
            messages.error(request, "Incorrect password. Try again.")

    return render(request, 'accounts/delete_account.html')


# Custom view for password change done
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"  # Point to your custom template