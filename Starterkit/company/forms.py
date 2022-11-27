from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = ()
        labels = {
            'address': 'Full Address',
            'contact': 'Contact Number'
        }
        widgets = {
            'address': forms.Textarea(attrs={'class':'form-control','rows':4, 'cols':15}),
            'contact': forms.TextInput(attrs={'class':'form-control',})
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        exclude = ('company',)
        labels = {
            'name': 'Full Name',
            'contact': 'Contact Number',
            'designation': 'Designation',
            'company': 'Company'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'contact': forms.TextInput(attrs={'class':'form-control'}),
            'designation': forms.TextInput(attrs={'class':'form-control'}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        labels = {
            'name': 'Company Name',
            'address': 'Address',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
        }

