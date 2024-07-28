from django import forms
from .models import PassCardAction, PassCardType, PassCard, PassCardIssue


class PassCardActionForm(forms.ModelForm):
    class Meta:
        model = PassCardAction
        fields = ['title']


class PassCardTypeForm(forms.ModelForm):
    class Meta:
        model = PassCardType
        fields = ['title']


class PassCardForm(forms.ModelForm):
    class Meta:
        model = PassCard
        fields = ['pass_id', 'pass_type']


 class PassCardIssueForm(forms.ModelForm):
     class Meta:
         model = PassCardIssue
         fields = ['issue_date', 'card', 'individual', 'description', 'action']
