from django import forms

from phonenumber_field.formfields import PhoneNumberField

from .models import Order

class AddToOrderForm(forms.Form):
    SIZE_CHOICES = [
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    CRUST_CHOICES = [
        ('thin', 'Thin'),
        ('thick', 'Thick'),
    ]

    size = forms.ChoiceField(choices = SIZE_CHOICES) 
    crust = forms.ChoiceField(choices = CRUST_CHOICES) 
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=99)

class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField(region='PL')
    city = forms.CharField()
    street = forms.CharField()
    house_number = forms.IntegerField()
    apartment_number = forms.IntegerField(required=False)
    comments = forms.CharField(required=False, widget=forms.Textarea)
    payment_method = forms.ChoiceField(choices = PAYMENT_CHOICES)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'city', 'street', 'house_number', 'apartment_number',
                  'comments', 'payment_method']