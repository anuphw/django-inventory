from django import forms
from .models import *
from django.forms.models import modelformset_factory



class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('status','order','probability')
    
StatusFormSet = modelformset_factory(Status,form=StatusForm,extra=0)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description']
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

ProductFormSet = modelformset_factory(Product,form=ProductForm,extra=0)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('client','contact_person','title','description','status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_person'].queryset = ClientContact.objects.none()

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = ProjectFiles
        fields = ('file','notes')
