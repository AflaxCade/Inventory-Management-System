from django import forms
from .models import Customer, Supplier, Category, Product, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm, UserCreationForm


class CreateUserForm(UserCreationForm):
    """
    Form for creating a new user with email validation.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password', 'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email
    

class CustomerForm(forms.ModelForm):
    """
    Form for creating and updating Customer instances.
    """
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}),

        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        qs = Customer.objects.exclude(id=self.instance.id).filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return email


class SupplierForm(forms.ModelForm):
    """
    Form for creating and updating Supplier instances.
    """
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name', 'required': True}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Name', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}),
        }


class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating Category instances.
    """
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'required': True}),
        }


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category', 'supplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category', 'required': True}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Supplier', 'required': True}),
        }


class OrderForm(forms.ModelForm):
    """
    Form for creating an Order instance.
    """

    class Meta:
        model = Order
        fields = ['customer', 'product', 'quantity', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Customer', 'required': True}),
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Product', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status', 'required': True}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom form for resetting password.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom form for setting a new password.
    """
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom form for changing the password.
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )