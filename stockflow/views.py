from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user
from .forms import CreateUserForm, CustomerForm
from .models import Customer

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            return redirect('login')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # get 'next' parameter from request
            next_url = request.GET.get('next')
            if next_url:  # if 'next' parameter exists, redirect to its value
                return redirect(next_url)
            else:  # if 'next' parameter does not exist, redirect to 'home'
                return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'dashboard.html', {})

@login_required(login_url='login')
def customer(request):

    customers = Customer.objects.all()
    context = {'customers': customers}

    return render(request, 'customer.html', context)

@login_required(login_url='login')
def profile(request):
    customer = request.user.customer
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    
    context = {'form': form, 'group': group}
    return render(request, 'profile.html', context)