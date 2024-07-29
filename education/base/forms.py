from django import forms
from .models import Individual


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = [
            'last_name', 'first_name', 'patronymic', 'gender', 'birth_date', 'social_insurance_number']
