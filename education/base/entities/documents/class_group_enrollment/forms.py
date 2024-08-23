from django import forms
from django_select2 import forms as s2forms
from ....generic_forms import DocumentForm, DocumentSubtableItemForm

from ....entities.documents.class_group_enrollment.models import ClassGroupEnrollment, ClassGroupEnrollmentItem
from ....entities.catalogs.student.models import Student
from ....entities.catalogs.class_group.models import ClassGroup


class ClassGroupEnrollmentItemForm(DocumentSubtableItemForm):
    class Meta:
        model = ClassGroupEnrollmentItem
        fields = ['class_group_enrollment', 'student', 'class_group']
        widgets = {
            'student': s2forms.ModelSelect2Widget(
                search_fields=[
                    "individual__last_name__icontains",
                    "individual__first_name__icontains",
                    "individual__patronymic__icontains",
                ],
                queryset=Student.objects.all().order_by('individual')
            ),
            'class_group': s2forms.ModelSelect2Widget(
                search_fields=["grade__icontains", "label__icontains"],
                queryset=ClassGroup.objects.all().order_by('grade'),
                attrs={
                    "data-minimum-input-length": 1
                }
            ),
        }


class ClassGroupEnrollmentForm(DocumentForm):

    class Meta:
        model = ClassGroupEnrollment
        fields = ['number', 'date', 'enrollment_date', 'comment']

    class_group_enrollment_list = forms.inlineformset_factory(
            ClassGroupEnrollment,
            ClassGroupEnrollmentItem,
            form=ClassGroupEnrollmentItemForm,
            extra=50,
            can_delete=True
        )
