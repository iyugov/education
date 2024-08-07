from django import forms
from .models import Student, ClassGroup, ClassGroupEnrollment, ClassGroupEnrollmentItem
from django.contrib.admin import widgets

from base.models import Individual


class StudentForm(forms.ModelForm):

    individual = forms.ModelChoiceField(
        label='Физическое лицо',
        queryset=Individual.objects.order_by('last_name', 'first_name', 'patronymic', 'birth_date')
    )

    class Meta:
        model = Student
        fields = ['individual']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ClassGroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClassGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ClassGroup
        fields = ['grade', 'label']


class ClassGroupEnrollmentItemForm(forms.ModelForm):
    class Meta:
        model = ClassGroupEnrollmentItem
        fields = ['class_group_enrollment', 'student', 'class_group']

    def __init__(self, *args, **kwargs):
        super(ClassGroupEnrollmentItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'


class ClassGroupEnrollmentForm(forms.ModelForm):

    class Meta:
        model = ClassGroupEnrollment
        fields = ['enrollment_date']

    def __init__(self, *args, **kwargs):
        super(ClassGroupEnrollmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class_group_enrollment_list = forms.inlineformset_factory(
            ClassGroupEnrollment,
            ClassGroupEnrollmentItem,
            form=ClassGroupEnrollmentItemForm,
            extra=40,
            can_delete=True
        )
