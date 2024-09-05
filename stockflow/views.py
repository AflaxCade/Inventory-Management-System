from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user
from .forms import CreateUserForm, CustomerForm, SupplierForm, CategoryForm, ProductForm, OrderForm, MultipleOrderForm
from .models import Customer, Supplier, Category, Product, Order, Invoice
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

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
    invoices = Invoice.objects.exclude(order__status='Cancelled').order_by('-id')[:10]
    context = {'invoices': invoices}
    return render(request, 'dashboard.html', context)


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
def customerOrders(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer does not exist.')
        return redirect('customer')
    orders = customer.order_set.all()
    pending_orders = orders.filter(status='Pending').count()
    shipped_orders = orders.filter(status='Shipped').count()
    delivered_orders = orders.filter(status='Delivered').count()
    cancelled_orders = orders.filter(status='Cancelled').count()
    context = {'customer': customer,
               'orders': orders,
               'pending_orders': pending_orders,
               'shipped_orders': shipped_orders,
               'delivered_orders': delivered_orders,
               'cancelled_orders': cancelled_orders,}
    return render(request, 'customer_orders.html', context)


@login_required(login_url='login')
def multipleOrders(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer does not exist.')
        return redirect('customer')

    OrderFormSet = inlineformset_factory(Customer, Order, form=MultipleOrderForm, extra=5)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    orders = formset.save(commit=False)
                    for order in orders:
                        product = order.product
                        
                        # Deduct product stock based on the validated form quantity
                        product.quantity -= order.quantity
                        product.save()

                        # Save the order
                        order.save()

                    formset.save_m2m()  # Save any many-to-many relationships if applicable
                    messages.success(request, 'Orders placed successfully.')
                    return redirect('customer_orders', pk=customer.id)
            except Exception as e:
                messages.error(request, f'Error saving orders: {e}')
        else:
            # Display form errors
            error_messages = []
            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f'{field}: {error}')
            if error_messages:
                messages.error(request, ' '.join(error_messages))

    context = {'formset': formset, 'customer': customer}
    return render(request, 'multiple_orders.html', context)


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


@login_required(login_url='login')
def order(request):
    orders = Order.objects.all()
    form = OrderForm()
    context = {'orders': orders, 'form': form}
    return render(request, 'order.html', context)


@login_required(login_url='login')
def process_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            product = order.product
            if order.quantity > product.quantity:
                messages.error(request, f'Not enough stock for {product.name}. Only {product.quantity} left.')
                return redirect('order')
            else:
                try:
                    with transaction.atomic():
                         # Update Product Quantity
                        product.quantity -= order.quantity
                        product.save()
                        # Save the Order
                        order.save()

                        # Create Invoice
                        invoice = Invoice(order=order, quantity=order.quantity, price=product.price, amount=product.price * order.quantity)
                        invoice.save()

                         # Success message
                        messages.success(request, 'Order placed successfully.')
                        return redirect('order')
                except Exception as e:
                    messages.error(request, f'Error processing the order: {e}')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    return redirect('order')


@login_required(login_url='login')
def updateOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        messages.error(request, 'Order does not exist.')
        return redirect('order')
    product = order.product
    current_quantity = order.quantity
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            quantity_difference = new_quantity - current_quantity
            if new_quantity > product.quantity + current_quantity:
                messages.error(request, f'Not enough stock for {product.name}. Only {product.quantity + current_quantity} available.')
                return redirect('order')
            else:
                try:
                    with transaction.atomic():
                       # Adjust product quantity based on the difference
                        product.quantity -= quantity_difference
                        product.save()

                        # Save the updated order
                        order = form.save()

                        # Update the invoice if necessary
                        order.invoice.amount = product.price * new_quantity
                        order.invoice.quantity = new_quantity
                        order.invoice.save()

                        # Success message
                        messages.success(request, 'Order updated successfully')
                        return redirect('order')
                except Exception as e:
                    messages.error(request, f'Error processing the order: {e}')
        else:
            error_message = form.errors.as_text()
            messages.error(request, f'{error_message}')
    form = OrderForm(instance=order)
    context = {'form': form, 'order': order}
    return render(request, 'edit_order.html', context)


@login_required(login_url='login')
def invoice(request):
    invoices = Invoice.objects.exclude(order__status='Cancelled')
    context = {'invoices': invoices}
    return render(request, 'invoice.html', context)