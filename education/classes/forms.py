from django import forms
from .models import Student, ClassGroup, ClassGroupEnrollment


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['individual']


class ClassGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ['grade', 'label']


class ClassGroupEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ClassGroupEnrollment
        fields = ['student', 'class_group', 'enrollment_date']
