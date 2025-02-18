from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CustomErrorList,
    CustomSetPasswordForm,
    CustomUserCreationForm,
    PasswordResetRequestForm,
)


def request_reset(request):
    template_data = {}
    template_data["title"] = "Forgot Password"
    if request.method == "GET":
        form = PasswordResetRequestForm()
        template_data["form"] = form
        return render(
            request, "accounts/request_reset.html", {"template_data": template_data}
        )
    elif request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.filter(username=username).first()
            if user:
                return redirect("accounts.reset_password", username=username)
            else:
                template_data["error"] = "Username not found."
        template_data["form"] = form
        return render(
            request, "accounts/request_reset.html", {"template_data": template_data}
        )


def reset_password(request, username):
    template_data = {}
    template_data["title"] = "Reset Password"
    user = get_object_or_404(User, username=username)
    if request.method == "GET":
        form = CustomSetPasswordForm(user)
        template_data["form"] = form
        return render(
            request, "accounts/reset_password.html", {"template_data": template_data}
        )
    elif request.method == "POST":
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            return redirect("accounts.login")
        template_data["form"] = form
        return render(
            request, "accounts/reset_password.html", {"template_data": template_data}
        )


@login_required
def orders(request):
    template_data = {}
    template_data["title"] = "Orders"
    template_data["orders"] = request.user.order_set.all()
    return render(request, "accounts/orders.html", {"template_data": template_data})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home.index")


def login(request):
    template_data = {}
    template_data["title"] = "Login"
    if request.method == "GET":
        return render(request, "accounts/login.html", {"template_data": template_data})
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            template_data["error"] = "The username or password is incorrect."
            return render(
                request, "accounts/login.html", {"template_data": template_data}
            )
        else:
            auth_login(request, user)
            return redirect("home.index")


def signup(request):
    template_data = {}
    template_data["title"] = "Sign Up"
    if request.method == "GET":
        template_data["form"] = CustomUserCreationForm()
        return render(request, "accounts/signup.html", {"template_data": template_data})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")
            user.save()
            return redirect("accounts.login")
        else:
            template_data["form"] = form
            return render(
                request, "accounts/signup.html", {"template_data": template_data}
            )


# Create your views here.
