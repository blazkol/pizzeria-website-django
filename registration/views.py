from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm, UserDetailsUpdateForm

""" def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context) """

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'Account created successfully!'

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        userdetails_form = UserDetailsUpdateForm(request.POST, instance=request.user.userdetails)
        if user_form.is_valid() and userdetails_form.is_valid():
            user_form.save()
            userdetails_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        userdetails_form = UserDetailsUpdateForm(instance=request.user.userdetails)

    context = {
        'user_form': user_form,
        'userdetails_form': userdetails_form,
    }
    return render(request, 'profile.html', context)

""" class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    success_message = 'Your account has been updated!'

    def get_object(self):
        return self.request.user """
