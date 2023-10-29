from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from .models import Pizza, Restaurant
from .forms import OrderForm, OrderItemForm

class MenuView(ListView):
    model = Pizza
    template_name = 'menu.html'
    context_object_name = 'pizza_list'
    ordering = ['price_medium']

class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'restaurants.html'
    context_object_name = 'restaurant_list'

def add_to_order(request, slug):
    pizza = Pizza.objects.get(slug=slug)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            if 'order' in request.session:
                for order_item in request.session['order']:
                    if order_item['id'] == form.cleaned_data.get('id') and \
                       order_item['size']  == form.cleaned_data.get('size')  and \
                       order_item['crust'] == form.cleaned_data.get('crust'):
                        order_item['quantity'] += form.cleaned_data.get('quantity')
                        break
                else:
                    request.session['order'].append(form.cleaned_data)
                request.session.modified = True
            else:
                request.session['order'] = [form.cleaned_data]
            messages.success(request, 'Your order has been updated!')
            return redirect('menu')
    else:
        form = OrderItemForm(initial={'id': pizza.id})

    context = {
        'pizza': pizza,
        'form': form,
    } 
    return render(request, 'add_to_order.html', context)

def order(request):
    order = request.session.get('order')
    if order:
        pizza_list = list(Pizza.objects.filter(id__in=[order_item['id'] for order_item in order]).values())
        order = sorted(order, key=lambda d: d['id'])
        for (order_item, pizza) in zip(order, pizza_list):
            order_item.update(pizza)
            order_item['price'] = order_item['quantity'] * order_item['price_medium'] if order_item['size'] == 'medium' else \
                                  order_item['quantity'] * order_item['price_large']
        context = {
            'order': order,
            'order_total_price': sum(order_item['price'] for order_item in order)
        }
    else:
        context = {}
    return render(request, 'order.html', context)

def order_confirm(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_complete')
    else:
        form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'order_confirm.html', context)

def order_complete(request):
    return render(request, 'order_complete.html')

