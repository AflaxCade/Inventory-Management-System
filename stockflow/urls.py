from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('', views.home, name='home'),
    path('customer/', views.customer, name='customer'),

    path('supplier/', views.supplier, name='supplier'),
    path('create_supplier/', views.createSupplier, name='create_supplier'),
    path('delete_supplier/<str:pk>/', views.deleteSupplier, name='delete_supplier'),
]
