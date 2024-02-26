import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, ListView, DetailView
from django.http import JsonResponse

from .models import Pizza, Restaurant, Order, OrderItem
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

class OrderHistoryView(ListView):
    template_name = 'order_history.html'
    context_object_name = 'order_list'
    paginate_by = 4

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')
    
class OrderDetailsView(DetailView):
    model = Order
    template_name = 'order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_item_list = OrderItem.objects.filter(order=self.kwargs['pk'])
        for order_item in order_item_list:
            order_item.price = order_item.quantity * order_item.pizza.price_medium if order_item.size == 'medium' else \
                                    order_item.quantity * order_item.pizza.price_large
            print(order_item.price)
        context['order_item_list'] = order_item_list
        context['order_total_price'] = sum(order_item.price for order_item in order_item_list)
        return context

class AddToOrderView(SuccessMessageMixin, FormView):
    form_class = OrderItemForm
    template_name = 'add_to_order.html'
    success_url = reverse_lazy('menu')
    success_message = 'Your order has been updated!'

    def dispatch(self, request, *args, **kwargs):
        self.pizza = Pizza.objects.get(slug=self.kwargs.get("slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['id'] = self.pizza.id
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizza'] = self.pizza
        return context
    
    def form_valid(self, form):
        if 'order' in self.request.session:
            for order_item in self.request.session['order']:
                if order_item['id'] == form.cleaned_data.get('id') and \
                   order_item['size']  == form.cleaned_data.get('size')  and \
                   order_item['crust'] == form.cleaned_data.get('crust'):
                    order_item['quantity'] += form.cleaned_data.get('quantity')
                    break
            else:
                self.request.session['order'].append(form.cleaned_data)
            self.request.session.modified = True
        else:
            self.request.session['order'] = [form.cleaned_data]
        return super().form_valid(form)

def order(request):
    if request.method == 'GET':
        if 'order' in request.session:
            order = sorted(request.session.get('order'), key=lambda d: d['id'])
            pizza_list = list(Pizza.objects.filter(id__in=[order_item['id'] for order_item in order]).values())
            for order_item in order:
                order_item.update(next((pizza for pizza in pizza_list if pizza['id'] == order_item['id']), None))
                order_item['price'] = order_item['quantity'] * order_item['price_medium'] if order_item['size'] == 'medium' else \
                                    order_item['quantity'] * order_item['price_large']
            context = {
                'order': order,
                'order_total_price': sum(order_item['price'] for order_item in order)
            }
        else:
            context = {}
        return render(request, 'order.html', context)
    
    elif request.method == 'DELETE':
        id_item_removed = json.load(request).get('id_item_removed')
        for order_item in request.session['order']:
            if order_item['id'] == id_item_removed:
                request.session['order'].remove(order_item)
                request.session.modified = True
        order = sorted(request.session.get('order'), key=lambda d: d['id'])
        pizza_list = list(Pizza.objects.filter(id__in=[order_item['id'] for order_item in order]).values())
        updated_total_price = 0
        for order_item in order:
            order_item.update(next((pizza for pizza in pizza_list if pizza['id'] == order_item['id']), None))
            updated_total_price += order_item['quantity'] * order_item['price_medium'] if order_item['size'] == 'medium' else \
                                order_item['quantity'] * order_item['price_large']
        return JsonResponse({'updated_total_price': updated_total_price})

def order_confirm(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                new_order = form.save(commit=False)
                new_order.user = request.user
                new_order.save()
            else:
                new_order = form.save()
            OrderItem.objects.bulk_create([OrderItem(
                order=new_order,
                pizza=Pizza.objects.get(pk=order_item['id']),
                size=order_item['size'],
                crust=order_item['crust'],
                quantity=order_item['quantity'],
            ) for order_item in request.session['order'] ])
            request.session['order'].clear()
            request.session.modified = True
            return redirect('order_complete')
    else:
        if request.user.is_authenticated:
            form = OrderForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone_number': request.user.userdetails.phone_number,
                'city': request.user.userdetails.city,
                'street': request.user.userdetails.street,
                'house_number': request.user.userdetails.house_number,
                'apartment_number': request.user.userdetails.apartment_number,
                })
            form.fields['email'].disabled = True 
        else:
            form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'order_confirm.html', context)

def order_complete(request):
    return render(request, 'order_complete.html')