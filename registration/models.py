from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(region='PL', null=True, blank=True)
    city = models.CharField(null=True, blank=True)
    street = models.CharField(null=True, blank=True)
    house_number = models.IntegerField(null=True, blank=True)
    apartment_number = models.IntegerField(null=True, blank=True)