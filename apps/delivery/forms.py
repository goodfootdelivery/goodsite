from django import forms
from django.forms import ModelForm, TextInput, Textarea, NumberInput, TimeInput
from .models import Address, SERVICES
from functools import partial

# Wed Dec  9 13:38:57 2015


class AddressForm(ModelForm):
    geocomplete = forms.CharField(label='Address')

    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'address': TextInput(attrs={
                'geo': 'formatted_address',
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
    ready_time = forms.TimeField(
        widget=TimeInput(format='%H:%M')
    )
    envelopes = forms.IntegerField(
        min_value=0,
        widget=NumberInput(attrs={
            'value': 0,
        })
    )
    rolls = forms.IntegerField(
        min_value=0,
        widget=NumberInput(attrs={
            'value': 0,
        })
    )
    boxes = forms.IntegerField(
        min_value=0,
        widget=NumberInput(attrs={
            'value': 0,
        })
    )


class ServiceForm(forms.Form):
    service = forms.ChoiceField(widget=forms.RadioSelect, choices=SERVICES)

