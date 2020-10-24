from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
import requests


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'ticket/signup.html', {'form': form, 'title': 'reqister here'})


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('dashboard')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'ticket/login.html', {'form': form, 'title': 'log in'})

@login_required(login_url='/login/')
def dashboard(request):
    u = User.objects.get(id=request.user.id)
    return render(request, 'ticket/dashboard.html', {"name": u})

@login_required(login_url='/login/')
def submit_ticket(request):
    u = User.objects.get(id=request.user.id)
    if "GET" == request.method:
        return render(request, "ticket/forms.html",{"name": u,"email":u.email})
    if request.method == 'POST':
        u = User.objects.get(id=request.user.id)
        Name = u,
        Email = u.email
        Department= request.POST.get("department")
        category = request.POST.get("category")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        Details = {'Name' : Name,
             'Email' :Email,
             'Department': Department,
             'category': category,
             'subject':subject,
             'description':description,
             'priority':priority}
        print(Details)
        messages.success(request, f' Ticket Submitted')
        return redirect('submit_form')