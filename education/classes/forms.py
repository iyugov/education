from django import forms
from .models import ClassGroup

class ClassGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ['grade', 'label']
