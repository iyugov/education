from django import forms
from .models import PassTag, PassTagRequest


class PassTagForm(forms.ModelForm):
    class Meta:
        model = PassTag
        fields = ['tag_id']


class PassTagRequestForm(forms.ModelForm):
    class Meta:
        model = PassTagRequest
        fields = ['requester', 'executor', 'request_date', 'comment']
