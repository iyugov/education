from django import forms

from ....entities.documents.class_group_enrollment.models import ClassGroupEnrollment, ClassGroupEnrollmentItem


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
        fields = ['number', 'date', 'enrollment_date']

    def __init__(self, *args, **kwargs):
        super(ClassGroupEnrollmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['number'].disabled = True

    class_group_enrollment_list = forms.inlineformset_factory(
            ClassGroupEnrollment,
            ClassGroupEnrollmentItem,
            form=ClassGroupEnrollmentItemForm,
            extra=40,
            can_delete=True
        )
