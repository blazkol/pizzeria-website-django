from django import forms

from .models import Restaurant, Order, OrderItem
 
class OrderForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['restaurant'].label_from_instance = self.label_from_instance
        self.fields['restaurant'].label = False
        self.fields['payment_method'].label = False

    @staticmethod
    def label_from_instance(obj):
        return '%s' % obj.city

    class Meta:
        model = Order
        exclude = ['user', 'date', 'status']

class OrderItemForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = OrderItem
        exclude = ['order', 'pizza']