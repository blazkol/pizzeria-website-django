from django.urls import path
from . import views

urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('add-to-order/<slug:slug>', views.add_to_order, name='add_to_order'),
    path('order/', views.order, name='order'),
    path('order/confirm', views.order_confirm, name='order_confirm'),
    path('order/complete', views.order_complete, name='order_complete'),
    path('profile/order-history/', views.order_history, name='order_history'),
    path('restaurants/', views.RestaurantsView.as_view(), name='restaurants'),
]