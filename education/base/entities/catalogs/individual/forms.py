from django import forms

from ....entities.catalogs.individual.models import Individual, ContactInfoItem


class ContactInfoItemForm(forms.ModelForm):
    class Meta:
        model = ContactInfoItem
        fields = ['individual', 'contact_info_type', 'value', 'comment']

    def __init__(self, *args, **kwargs):
        super(ContactInfoItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'


class IndividualForm(forms.ModelForm):

    is_student = forms.BooleanField(required=False, label='Обучающийся')

    class Meta:
        model = Individual
        fields = [
            'code', 'last_name', 'first_name', 'patronymic', 'gender', 'birth_date', 'social_insurance_number',
            'comment']

    contact_info_list = forms.inlineformset_factory(
        Individual,
        ContactInfoItem,
        form=ContactInfoItemForm,
        extra=3,
        can_delete=True
    )

    def __init__(self, *args, **kwargs):
        super(IndividualForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field, forms.BooleanField):
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
        self.fields['code'].disabled = True


class IndividualCSVUploadForm(forms.Form):

    csv_file = forms.FileField(label='Файл CSV')

    set_students = forms.BooleanField(required=False, label='Обучающиеся')

    def __init__(self, *args, **kwargs):
        super(IndividualCSVUploadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field, forms.BooleanField):
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
