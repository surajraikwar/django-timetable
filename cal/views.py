from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from cal.forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Account, TimeTable, TimeTableItem
from django.http import HttpResponseRedirect


'''
home page -
guest users gets option to login or signing up
and after logging in user gets muliple choice of options for creating is Public portfolio
'''


def index(request):
    user = request.user
    if user.is_authenticated:
        days = TimeTable.objects.all()
        for day in days:
            periods = TimeTableItem.objects.all()
            return render(request, 'cal/index.html', {'periods': periods, 'days':days})
    else:
        return render(request, 'cal/index.html')


'''
Signup with name, email and password
'''


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            account = authenticate(email=email, password=password)
            login(request, account)
            return redirect('index')

        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'cal/registration.html', context)


'''
registered user can login with his email and password
'''


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('index')
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')

    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request, 'cal/login.html', context)


'''
logged in user can logout
'''


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
