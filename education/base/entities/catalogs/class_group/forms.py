from django import forms

from ....entities.catalogs.class_group.models import ClassGroup


class ClassGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClassGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True

    class Meta:
        model = ClassGroup
        fields = ['code', 'grade', 'label']
