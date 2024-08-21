from django import forms

from ....entities.catalogs.contact_info_type.models import ContactInfoType


class ContactInfoTypeForm(forms.ModelForm):
    class Meta:
        model = ContactInfoType
        fields = ['code', 'title']

    def __init__(self, *args, **kwargs):
        super(ContactInfoTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True
