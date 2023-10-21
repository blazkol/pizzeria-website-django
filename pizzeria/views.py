from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from .models import Pizza
from .forms import AddToOrderForm

""" def menu(request):
    pizza_list = Pizza.objects.order_by('price_medium')
    context = {
        'pizza_list': pizza_list,
    }
    return render(request, 'menu.html', context) """

class MenuView(ListView):
    model = Pizza
    template_name = 'menu.html'
    context_object_name = 'pizza_list'
    ordering = ['price_medium']

def add_to_order(request, slug):
    pizza = Pizza.objects.get(slug=slug)
    if request.method == 'POST':
        form = AddToOrderForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Your order has been updated!')
            return redirect('menu')
    else:
        form = AddToOrderForm()

    context = {
        'pizza': pizza,
        'form': form,
    } 
    return render(request, 'add_to_order.html', context)

