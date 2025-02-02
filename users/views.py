from django.shortcuts import render 
from django.urls import reverse , reverse_lazy
from django.contrib.auth.views import LoginView 
from django.views.generic.edit import CreateView , FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import login

# Create your views here.

from .models import EmailUser
from .forms import EmailUserCreation


class EmailLogin(LoginView):
    template_name="users/login.html"
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy("account_selection")



class EmailSignup(FormView ,UserPassesTestMixin ):
    form_class=EmailUserCreation
    template_name="users/signup.html"
    success_url = reverse_lazy("account_selection")

    def test_func(self):
        return self.request.user.is_anonymous
    
    def form_valid(self, form):
        user = form.save()
        login(self.request , user)
        return super().form_valid(form)
    



