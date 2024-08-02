from django import forms
from .models import Student, ClassGroup, ClassGroupEnrollment
from django.contrib.admin import widgets


class StudentForm(forms.ModelForm):
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


class ClassGroupEnrollmentForm(forms.ModelForm):

    class Meta:
        model = ClassGroupEnrollment
        fields = ['student', 'class_group', 'enrollment_date']

    def __init__(self, *args, **kwargs):
        super(ClassGroupEnrollmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'