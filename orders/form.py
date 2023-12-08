from django import forms

from orders.models import Orders


class OrdersForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'John'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Smith'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'you_email@example.com'
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'street name and number'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    plz = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:

        model = Orders
        fields = ('first_name', 'last_name', 'email', 'street', 'city', 'plz')
