from django import forms

from ....entities.catalogs.pass_tag.models import PassTag


class PassTagForm(forms.ModelForm):
    class Meta:
        model = PassTag
        fields = ['code', 'tag_id']

    def __init__(self, *args, **kwargs):
        super(PassTagForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True


class PassTagCSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Файл CSV')

    def __init__(self, *args, **kwargs):
        super(PassTagCSVUploadForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'