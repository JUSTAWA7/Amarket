from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import RegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"