from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class Pizza(models.Model):
    name = models.CharField(default = "")
    ingredients = models.CharField(default = "")
    price_medium = models.FloatField(default = 0.00)
    price_large = models.FloatField(default = 0.00)
    slug = models.SlugField(default="")

class Restaurant(models.Model):
    city = models.CharField(default = "")
    address = models.CharField(default = "")
    phone_number = PhoneNumberField(default = "")

class Order(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    phone_number = PhoneNumberField(region='PL')
    city = models.CharField()
    street = models.CharField()
    house_number = models.IntegerField()
    apartment_number = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    payment_method = models.CharField() 

