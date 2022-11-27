from django import forms
from .models import *
from clients.models import Client, ClientContact



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
