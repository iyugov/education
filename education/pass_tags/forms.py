from django import forms
from .models import PassTag, PassTagRequest, PassTagRequestItem


class PassTagForm(forms.ModelForm):
    class Meta:
        model = PassTag
        fields = ['tag_id']

    def __init__(self, *args, **kwargs):
        super(PassTagForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PassTagRequestItemForm(forms.ModelForm):
    class Meta:
        model = PassTagRequestItem
        fields = ['pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status']

    def __init__(self, *args, **kwargs):
        super(PassTagRequestItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'


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

    def __init__(self, *args, **kwargs):
        super(PassTagRequestForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
