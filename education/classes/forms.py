from django import forms
from .models import ClassGroup, ClassGroupEnrollment


class ClassGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ['grade', 'label']


class ClassGroupEnrollmentForm(forms.ModelForm):
    class Meta:
        model = ClassGroupEnrollment
        fields = ['student', 'class_group', 'enrollment_date']
