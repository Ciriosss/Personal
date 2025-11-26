from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login


def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            username = form.cleaned_data.get('username')
            login(request, user) 
            messages.success(request,'Congratulations {}! your account has been created successfully, now you are able to log-in'.format(username))
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'user/sign-up.html', {'form': form})
