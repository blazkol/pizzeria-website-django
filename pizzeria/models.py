from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

class Pizza(models.Model):
    name = models.CharField(unique=True)
    ingredients = models.CharField()
    price_medium = models.FloatField()
    price_large = models.FloatField()
    slug = models.SlugField()

class Restaurant(models.Model):
    phone_number = PhoneNumberField()
    city = models.CharField()
    address = models.CharField()

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    STATUS_CHOICES = [
        ('in progress', 'In progress'),
        ('in delivery', 'In delivery'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    phone_number = PhoneNumberField(region='PL')
    city = models.CharField()
    street = models.CharField()
    house_number = models.IntegerField()
    apartment_number = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    payment_method = models.CharField(choices = PAYMENT_CHOICES, default='cash')
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices = STATUS_CHOICES, default='in progress')

class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    CRUST_CHOICES = [
        ('thin', 'Thin'),
        ('thick', 'Thick'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.CharField(choices = SIZE_CHOICES, default='medium')
    crust = models.CharField(choices = CRUST_CHOICES, default='thin')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(99)])