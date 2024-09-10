from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('', views.home, name='home'),
    path('customer/', views.customer, name='customer'),
    path('customer/<str:pk>/', views.customerOrders, name='customer_orders'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name='delete_customer'),

    path('supplier/', views.supplier, name='supplier'),
    path('create_supplier/', views.createSupplier, name='create_supplier'),
    path('supplier/<str:pk>/', views.updateSupplier, name='update_supplier'),
    path('delete_supplier/<str:pk>/', views.deleteSupplier, name='delete_supplier'),

    path('category/', views.category, name='category'),
    path('create_category/', views.createCategory, name='create_category'),
    path('update_category/<str:pk>/', views.updateCategory, name='update_category'),
    path('delete_category/<str:pk>/', views.deleteCategory, name='delete_category'),

    path('product/', views.product, name='product'),
    path('product/<str:pk>/', views.updateProduct, name='update_product'),
    path('create_product/', views.createProduct, name='create_product'),
    path('delete_product/<str:pk>/', views.deleteProduct, name='delete_product'),

    path('order/', views.order, name='order'),
    path('create_order/', views.process_order, name='create_order'),
    path('multiple_orders/<str:pk>/', views.multipleOrders, name='multiple_orders'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),


    path('invoice/', views.invoice, name='invoice'),
    path('invoice_details/<str:pk>/', views.invoiceDetails, name='invoice_details'),

    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html", form_class=CustomPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html", form_class=CustomSetPasswordForm),name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html', form_class=CustomPasswordChangeForm), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
]
