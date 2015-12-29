from django import forms
from django.forms import ModelForm, TextInput, Textarea, NumberInput, TimeInput
from .models import Address, Parcel
from .delivery import SERVICES, PARCELS

# Tue Dec 29 15:31:41 2015


class AddressForm(ModelForm):
    geocomplete = forms.CharField(label='Address')

    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'formatted': TextInput(attrs={
                'geo': 'formatted_address',
                'type': 'hidden',
            }),
            'number': TextInput(attrs={
                'geo': 'street_number',
                'type': 'hidden',
            }),
            'street': TextInput(attrs={
                'geo': 'route',
                'type': 'hidden',
            }),
            'locality': TextInput(attrs={
                'geo': 'locality',
                'type': 'hidden',
            }),
            'postal_code': TextInput(attrs={
                'geo': 'postal_code',
                'type': 'hidden',
            }),
            'region': TextInput(attrs={
                'geo': 'administrative_area_level_1',
                'type': 'hidden',
            }),
            'country': TextInput(attrs={
                'geo': 'country',
                'type': 'hidden',
            }),
            'location': TextInput(attrs={
                'geo': 'location',
                'type': 'hidden',
            }),
            'comments': Textarea(attrs={
                'rows': 2
            }),
        }


class OrderForm(forms.Form):
    delivery_date = forms.DateField()
    ready_time = forms.TimeField(widget=TimeInput(format='%H:%M'))
    parcel = forms.ChoiceField(widget=forms.RadioSelect, choices=PARCELS)


class ParcelForm(ModelForm):
    class Meta:
        model = Parcel


class ServiceForm(forms.Form):
    service = forms.ChoiceField(widget=forms.RadioSelect, choices=SERVICES)
