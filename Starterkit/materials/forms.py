from django import forms
from django.forms.models import modelformset_factory
from .models import *
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'

class MaterialQtyForm(forms.ModelForm):
    class Meta:
        model = MaterialQty
        fields = ['material','quantity','price']
    
    def __init__(self, *args, **kwargs):
        super(MaterialQtyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['date','description','supplier','warehouse','project']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

MaterialFormSet = modelformset_factory(MaterialQty,form=MaterialQtyForm,extra=0)

# For Transfer
class MaterialQtyTransferForm(forms.ModelForm):
    class Meta:
        model = MaterialQtyTransfer
        fields = ['material','quantity']
    
    def __init__(self, *args, **kwargs):
        super(MaterialQtyTransferForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TransferForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })  

    class Meta:
        model = MaterialTransfer
        fields = ['date','source','destination','project']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date','class':'form-control'})
        }

    
    
        
    

TransferFormSet = modelformset_factory(MaterialQtyTransfer,form=MaterialQtyTransferForm,extra=0)


