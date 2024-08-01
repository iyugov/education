from django import forms
from .models import PassTag, PassTagRequest, PassTagRequestItem


class PassTagForm(forms.ModelForm):
    class Meta:
        model = PassTag
        fields = ['tag_id']


class PassTagRequestItemForm(forms.ModelForm):
    class Meta:
        model = PassTagRequestItem
        fields = ['pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status']


class PassTagRequestForm(forms.ModelForm):
    class Meta:
        model = PassTagRequest
        fields = ['requester', 'executor', 'request_date', 'comment']

    pass_tag_request_item_list = forms.inlineformset_factory(
        PassTagRequest,
        PassTagRequestItem,
        form=PassTagRequestItemForm,
        extra=1,
        can_delete=True
    )
