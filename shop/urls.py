from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('order/create/', views.OrderCreateView.as_view(), name='order-create'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('product/<int:product_id>/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('register/', views.RegisterView.as_view(), name='register'),
]