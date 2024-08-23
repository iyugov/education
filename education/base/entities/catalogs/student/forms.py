from django_select2 import forms as s2forms

from ....generic_forms import CatalogForm

from ....entities.catalogs.student.models import Student
from ....entities.catalogs.individual.models import Individual


class StudentForm(CatalogForm):

    class Meta:
        model = Student
        fields = ['code', 'individual']
        widgets = {
            'individual': s2forms.ModelSelect2Widget(
                search_fields=["last_name__icontains", "first_name__icontains", "patronymic__icontains"],
                queryset=Individual.objects.filter(rel_student__isnull=True).order_by('last_name', 'first_name', 'patronymic')
            ),
        }
