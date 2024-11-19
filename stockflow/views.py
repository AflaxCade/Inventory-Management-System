from decimal import Decimal
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, CustomerForm, SupplierForm, CategoryForm, ProductForm, OrderForm, MultipleOrderForm
from .models import Customer, Supplier, Category, Product, Order, Invoice
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import uuid
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
@admin_only
def home(request):
    orders = Order.objects.select_related('product', 'customer').order_by('-id')[:10]
    context = {'orders': orders}
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer = request.user.customer
    orders = customer.order_set.select_related('product', 'customer').all()

    order_counts = orders.aggregate(
        pending_orders=Count('id', filter=Q(status='Pending')),
        shipped_orders=Count('id', filter=Q(status='Shipped')),
        delivered_orders=Count('id', filter=Q(status='Delivered')),
    )

    invoices = Invoice.objects.filter(customer=customer).count()

    context = {
        'orders': orders,
        'invoices': invoices,
        'pending_orders': order_counts['pending_orders'],
        'shipped_orders': order_counts['shipped_orders'],
        'delivered_orders': order_counts['delivered_orders'],
    }
    return render(request, 'user_page.html', context)


@login_required(login_url='login')
def profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        messages.error(request, 'Admins do not have a customer profile.')
        previous_url = request.META.get('HTTP_REFERER', 'home')  # 'default_view' is the fallback
        return redirect(previous_url)
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
@allowed_users(allowed_roles=['admin'])
def customer(request):
    customers = Customer.objects.all()
    form = CustomerForm()
    context = {'customers': customers, 'form': form}

    return render(request, 'customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        messages.success(request, f'{customer.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Customer does not exist.')
    return redirect('customer')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customerOrders(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer does not exist.')
        return redirect('customer')
    orders = customer.order_set.select_related('product', 'customer').all()
    invoices = Invoice.objects.filter(customer=customer).count()
    order_counts = orders.aggregate(
        pending_orders=Count('id', filter=Q(status='Pending')),
        shipped_orders=Count('id', filter=Q(status='Shipped')),
        delivered_orders=Count('id', filter=Q(status='Delivered')),
    )
    context = {'customer': customer,
                'orders': orders,
                'invoices': invoices,
                'pending_orders': order_counts['pending_orders'],
                'shipped_orders': order_counts['shipped_orders'],
                'delivered_orders': order_counts['delivered_orders'],}
    return render(request, 'customer_orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def supplier(request):
    suppliers = Supplier.objects.all()
    form = SupplierForm()
    context = {'suppliers': suppliers, 'form': form}
    return render(request, 'supplier.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteSupplier(request, pk):
    try:
        supplier = Supplier.objects.get(id=pk)
        supplier.delete()
        messages.success(request, f'{supplier.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Supplier does not exist.')
    return redirect('supplier')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def category(request):
    categories = Category.objects.all()
    form = CategoryForm()
    context = {'categories': categories, 'form': form}
    return render(request, 'category.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteCategory(request, pk):
    try:
        category = Category.objects.get(id=pk)
        category.delete()
        messages.success(request, f'{category.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Category does not exist.')
    return redirect('category')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.select_related('category', 'supplier').all()
    form = ProductForm()
    context = {'products': products, 'form': form}
    return render(request, 'product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    try:
        product = Product.objects.select_related('category', 'supplier').get(id=pk)
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
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        messages.success(request, f'{product.name} deleted successfully.')
    except ObjectDoesNotExist:
        messages.error(request, 'Product does not exist.')
    return redirect('product')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order(request):
    orders = Order.objects.all()
    form = OrderForm()
    context = {'orders': orders, 'form': form}
    return render(request, 'order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def multipleOrders(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer does not exist.')
        return redirect('customer')

    OrderFormSet = inlineformset_factory(Customer, Order, form=MultipleOrderForm, extra=10)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    orders = formset.save(commit=False)
                    total_amount = 0
                    for order in orders:
                        product = order.product
                        product.quantity -= order.quantity
                        product.save()

                        order.save()
                        total_amount += order.product.price * order.quantity
                    
                    formset.save_m2m()

                    # Create the invoice
                    invoice_number = str(uuid.uuid4()).replace('-', '').upper()[:10]  # Generate unique invoice number
                    invoice = Invoice.objects.create(
                        customer=customer,
                        total_amount=total_amount,
                        invoice_number=invoice_number,
                    )
                    invoice.orders.set(orders)

                    messages.success(request, 'Orders placed successfully and Invoice created.')
                    return redirect('customer_orders', pk=customer.id)
            except Exception as e:
                messages.error(request, f'Error saving orders: {e}')
        else:
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
@allowed_users(allowed_roles=['admin'])
def singleOrder(request):
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
                        total_amount = order.product.price * order.quantity
                        invoice_number = str(uuid.uuid4()).replace('-', '').upper()[:10]  # Generate unique invoice number
                        invoice = Invoice.objects.create(
                            customer=order.customer,
                            total_amount=total_amount,
                            invoice_number=invoice_number
                        )
                        invoice.orders.add(order)  # Add the order to the invoice

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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin', 'customer'])
def invoice(request):
    if request.user.is_staff:
        invoices = Invoice.objects.select_related('customer').prefetch_related('orders')
    else:
        invoices = Invoice.objects.filter(customer=request.user.customer).select_related('customer').prefetch_related('orders')
    context = {'invoices': invoices}
    return render(request, 'invoice.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def invoiceDetails(request, pk):
    try:
        invoice = Invoice.objects.get(id=pk)

        # Restrict access for non-staff users to only their own invoices
        if not request.user.is_staff and invoice.customer != request.user.customer:
            messages.error(request, 'You do not have permission to view this invoice.')
            return redirect('invoice')
        
    except Invoice.DoesNotExist:
        messages.error(request, 'Invoice does not exist.')
        return redirect('invoice')
    
    orders = invoice.orders.all()
    vat_rate = Decimal('0.05')  # 5% VAT
    vat_total = 0
    total_amount = 0
    
    for order in orders:
        order.sub_total = order.quantity * order.product.price
        order.sub_vat = order.sub_total * vat_rate
        order.sub_total_sub_vat = order.sub_total + order.sub_vat
        vat_total += order.sub_total * vat_rate
        total_amount += order.sub_total

    total_with_vat = total_amount + vat_total

    # Update the total amount of the invoice if it is different from the calculated total amount
    if total_amount != invoice.total_amount:
        invoice.total_amount = total_amount
        invoice.save()
        
    context = {
        'invoice': invoice,
        'orders': orders,
        'vat_total': vat_total,
        'total_with_vat': total_with_vat,
    }
    return render(request, 'invoice_template.html', context)