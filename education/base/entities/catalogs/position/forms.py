from django import forms

from ....entities.catalogs.position.models import Position


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = ['code', 'title']

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True
