from django import forms
from django.forms.models import modelformset_factory
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class MaterialQtyForm(forms.ModelForm):
    class Meta:
        model = MaterialQty
        fields = ['material','quantity']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['date','description','supplier','warehouse','project']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

MaterialFormSet = modelformset_factory(MaterialQty,form=MaterialQtyForm,extra=0)

# For Transfer
class MaterialQtyTransferForm(forms.ModelForm):
    class Meta:
        model = MaterialQtyTransfer
        fields = ['material','quantity']

class TransferForm(forms.ModelForm):
    class Meta:
        model = MaterialTransfer
        fields = ['date','source','destination','project']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

TransferFormSet = modelformset_factory(MaterialQtyTransfer,form=MaterialQtyTransferForm,extra=0)