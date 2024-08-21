from django import forms

from ....entities.catalogs.employee.models import Employee, PositionItem
from ....entities.catalogs.individual.models import Individual


class PositionItemForm(forms.ModelForm):
    class Meta:
        model = PositionItem
        fields = ['employee', 'position', 'is_main']

    def __init__(self, *args, **kwargs):
        super(PositionItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if isinstance(widget, forms.widgets.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'

class EmployeeForm(forms.ModelForm):

    individual = forms.ModelChoiceField(
        label='Физическое лицо',
        queryset=Individual.objects.order_by('last_name', 'first_name', 'patronymic', 'birth_date')
    )

    class Meta:
        model = Employee
        fields = ['code', 'individual']

    position_list = forms.inlineformset_factory(
        Employee,
        PositionItem,
        form=PositionItemForm,
        extra=1,
        can_delete=True
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True
