from django import forms

from ....entities.catalogs.student.models import Student
from ....entities.catalogs.individual.models import Individual


class StudentForm(forms.ModelForm):

    individual = forms.ModelChoiceField(
        label='Физическое лицо',
        queryset=Individual.objects.order_by('last_name', 'first_name', 'patronymic', 'birth_date')
    )

    class Meta:
        model = Student
        fields = ['code', 'individual']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True
