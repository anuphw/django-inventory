from django import forms
from django.forms.models import modelformset_factory
from .models import *
from django.core.exceptions import ValidationError


class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        fields = '__all__'



