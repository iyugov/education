from django import forms

from ..models.pass_tag import PassTag


class PassTagForm(forms.ModelForm):
    class Meta:
        model = PassTag
        fields = ['tag_id']

    def __init__(self, *args, **kwargs):
        super(PassTagForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
