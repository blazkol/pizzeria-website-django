from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=50, default = "")
    ingredients = models.CharField(max_length=250, default = "")
    price_medium = models.FloatField(max_length=5, default = 0.00)
    price_large = models.FloatField(max_length=5, default = 0.00)
    slug = models.SlugField(default="", null=False)