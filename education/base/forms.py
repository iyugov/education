from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Individual, ContactInfoType, ContactInfoItem


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
