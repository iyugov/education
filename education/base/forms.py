from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Individual, ContactInfoType, ContactInfoItem

from education.metadata import has_dependencies


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
            'last_name', 'first_name', 'patronymic', 'gender', 'birth_date', 'social_insurance_number', 'comment']

    contact_info_list = forms.inlineformset_factory(
        Individual,
        ContactInfoItem,
        form=ContactInfoItemForm,
        extra=1,
        can_delete=True
    )

    def __init__(self, *args, **kwargs):
        super(IndividualForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field, forms.BooleanField):
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
        if self.instance.pk and hasattr(self.instance, 'student'):
            self.fields['is_student'].initial = True
            if has_dependencies(self.instance.student):
                self.fields['is_student'].widget.attrs['disabled'] = 'disabled'


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


class ContactInfoTypeForm(forms.ModelForm):
    class Meta:
        model = ContactInfoType
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(ContactInfoTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
