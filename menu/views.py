from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Pizza

def menu(request):
    pizza_list = Pizza.objects.order_by('-name')
    template = loader.get_template('menu.html') 
    context = {
        'pizza_list': pizza_list,
    }
    return HttpResponse(template.render(context, request))
