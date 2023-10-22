from django.contrib import admin

from .models import Pizza, Restaurant, Order

class PizzaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Restaurant)
admin.site.register(Order)
