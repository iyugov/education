from django import forms
from django_select2 import forms as s2forms
from ....generic_forms import CatalogForm, CatalogSubtableItemForm

from ....entities.catalogs.employee.models import Employee, PositionItem
from ....entities.catalogs.individual.models import Individual


class PositionItemForm(CatalogSubtableItemForm):
    class Meta:
        model = PositionItem
        fields = ['employee', 'position', 'is_main']


class EmployeeForm(CatalogForm):

    class Meta:
        model = Employee
        fields = ['code', 'individual']
        widgets = {
            'individual': s2forms.ModelSelect2Widget(
                search_fields=["last_name__icontains", "first_name__icontains", "patronymic__icontains"],
                queryset=Individual.objects.filter(rel_employee__isnull=True).order_by('last_name', 'first_name', 'patronymic')
            )
        }

    position_list = forms.inlineformset_factory(
        Employee,
        PositionItem,
        form=PositionItemForm,
        extra=1,
        can_delete=True
    )

