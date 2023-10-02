from django.shortcuts import render

from .models import Pizza

def menu(request):
    pizza_list = Pizza.objects.order_by('price_medium')
    context = {
        'pizza_list': pizza_list,
    }
    return render(request, 'menu.html', context)
