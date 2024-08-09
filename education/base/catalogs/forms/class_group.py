from django import forms

from ..models.class_group import ClassGroup


class ClassGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClassGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ClassGroup
        fields = ['grade', 'label']
