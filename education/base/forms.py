from django import forms
from .models import Individual, ContactInfoType, ContactInfoItem


class ContactInfoItemForm(forms.ModelForm):
    class Meta:
        model = ContactInfoItem
        fields = ['individual', 'contact_info_type', 'value']


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = [
            'last_name', 'first_name', 'patronymic', 'gender', 'birth_date', 'social_insurance_number']

    contact_info_list = forms.inlineformset_factory(
        Individual,
        ContactInfoItem,
        form=ContactInfoItemForm,
        extra=3,
        can_delete=True
    )


class ContactInfoTypeForm(forms.ModelForm):
    class Meta:
        model = ContactInfoType
        fields = ['title']
