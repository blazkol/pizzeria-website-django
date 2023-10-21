from django import forms

class AddToOrderForm(forms.Form):
    SIZE_CHOICES = [
        ('1', 'Medium'),
        ('2', 'Large'),
    ]
    CRUST_CHOICES = [
        ('1', 'Thin'),
        ('2', 'Thick'),
    ]
    size = forms.ChoiceField(choices = SIZE_CHOICES) 
    crust = forms.ChoiceField(choices = CRUST_CHOICES) 
    quantity = forms.IntegerField(initial=0, min_value=0, max_value=99)