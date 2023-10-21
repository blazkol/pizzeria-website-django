from django.contrib import admin

from .models import Pizza

class PizzaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

admin.site.register(Pizza, PizzaAdmin)
