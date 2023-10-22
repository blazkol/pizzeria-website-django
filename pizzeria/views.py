from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView

from .models import Pizza, Restaurant
from .forms import AddToOrderForm, OrderForm

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
        form = AddToOrderForm(request.POST)
        if form.is_valid():
            order_item = {'name': pizza.name}
            order_item.update(form.cleaned_data)
            if 'order' in request.session:
                for i in request.session['order']:
                    if i['name'] == order_item['name'] and i['size'] == order_item['size'] and i['crust'] == order_item['crust']:
                        i['quantity'] += order_item['quantity']
                        break
                else:
                    request.session['order'].append(order_item)
                request.session.modified = True
            else:
                request.session['order'] = [order_item]
            print(request.session['order'])
            messages.success(request, 'Your order has been updated!')
            return redirect('menu')
    else:
        form = AddToOrderForm()

    context = {
        'pizza': pizza,
        'form': form,
    } 
    return render(request, 'add_to_order.html', context)

def order(request):
    order = request.session.get('order')
    context = {
        'order': order,
    }
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

