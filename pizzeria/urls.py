from django.urls import path
from . import views

urlpatterns = [
    path("", views.MenuView.as_view(), name="menu"),
    path("add-to-order/<slug:slug>", views.add_to_order, name="add-to-order"),
]