from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user
from .forms import CreateUserForm, CustomerForm, SupplierForm, CategoryForm, ProductForm
from .models import Customer, Supplier, Category, Product
from django.core.exceptions import ObjectDoesNotExist

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
    return render(request, 'account/register.html', context)

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
    return render(request, 'account/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'dashboard.html', {})


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
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    
    context = {'form': form, 'group': group}
    return render(request, 'account/profile.html', context)


@login_required(login_url='login')
def customer(request):

    customers = Customer.objects.all()
    form = CustomerForm()
    context = {'customers': customers, 'form': form}

    return render(request, 'customer.html', context)


@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully')
            return redirect('customer')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    return redirect('customer')


@login_required(login_url='login')
def updateCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer does not exist.')
        return redirect('customer')
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully')
            return redirect('customer')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
            return redirect('customer')
    context = {'form': form, 'customer': customer}
    return render(request, 'customer.html', context)
    

@login_required(login_url='login')
def deleteCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        messages.success(request, f'{customer.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Customer does not exist.')
    return redirect('customer')


@login_required(login_url='login')
def supplier(request):
    suppliers = Supplier.objects.all()
    form = SupplierForm()
    context = {'suppliers': suppliers, 'form': form}
    return render(request, 'supplier.html', context)


@login_required(login_url='login')
def createSupplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully')
            return redirect('supplier')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    return redirect('supplier')


@login_required(login_url='login')
def updateSupplier(request, pk):
    try:
        supplier = Supplier.objects.get(id=pk)
    except Supplier.DoesNotExist:
        messages.error(request, 'Supplier does not exist.')
        return redirect('supplier')
    form = SupplierForm(instance=supplier)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully')
            return redirect('supplier')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    context = {'form': form, 'supplier': supplier}
    return render(request, 'edit_supplier.html', context)


@login_required(login_url='login')
def deleteSupplier(request, pk):
    try:
        supplier = Supplier.objects.get(id=pk)
        supplier.delete()
        messages.success(request, f'{supplier.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Supplier does not exist.')
    return redirect('supplier')


@login_required(login_url='login')
def category(request):
    categories = Category.objects.all()
    form = CategoryForm()
    context = {'categories': categories, 'form': form}
    return render(request, 'category.html', context)


@login_required(login_url='login')
def createCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully')
            return redirect('category')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    return redirect('category')


@login_required(login_url='login')
def updateCategory(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        messages.error(request, 'Category does not exist.')
        return redirect('category')
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('category')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
            return redirect('category')
    context = {'form': form, 'category': category}
    return render(request, 'category.html', context)


@login_required(login_url='login')
def deleteCategory(request, pk):
    try:
        category = Category.objects.get(id=pk)
        category.delete()
        messages.success(request, f'{category.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Category does not exist.')
    return redirect('category')


@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    form = ProductForm()
    context = {'products': products, 'form': form}
    return render(request, 'product.html', context)


@login_required(login_url='login')
def createProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully')
            return redirect('product')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    return redirect('product')

@login_required(login_url='login')
def updateProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        messages.error(request, 'Product does not exist.')
        return redirect('product')
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    context = {'form': form, 'product': product}
    return render(request, 'edit_product.html', context)


@login_required(login_url='login')
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        messages.success(request, f'{product.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Product does not exist.')
    return redirect('product')