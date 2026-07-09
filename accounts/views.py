from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("blog:post-list")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


class UserLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return "/"


def logout_view(request):

    logout(request)

    return redirect("blog:post-list")