from django import forms

from ....objects.catalogs.contact_info_type.models import ContactInfoType


class ContactInfoTypeForm(forms.ModelForm):
    class Meta:
        model = ContactInfoType
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(ContactInfoTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
