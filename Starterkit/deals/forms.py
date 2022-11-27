from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = "__all__"
        exclude = ()
        labels = {
            'status_col': _('Status Column Number'),
        }
        widgets = {
            'status_col': forms.NumberInput(attrs={'class':'form-control'}),
            'status': forms.TextInput(attrs={'class':'form-control'})
        }

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = "__all__"
        exclude = ()
        labels = {
            'contact_person': 'Contact Person',
            'title': 'Title',
            'description': 'Description',
            'status': 'Status',
            'delivery_address': 'Delivery Address'
        }
        widgets = {
            'contact_person': forms.TextInput(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'Description': forms.Textarea(attrs={'class':'form-control'}),
        }
