from django import forms
from django_select2 import forms as s2forms


class CatalogForm(forms.ModelForm):

    dummy = forms.ChoiceField(widget=s2forms.ModelSelect2Widget, required=False)

    def __init__(self, *args, **kwargs):
        super(CatalogForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if isinstance(visible.field.widget, forms.widgets.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(visible.field.widget, s2forms.ModelSelect2Widget):
                visible.field.widget.attrs['data-allow-clear'] = 'true'
                visible.field.widget.attrs['data-placeholder'] = '---'
        if hasattr(self, 'code'):
            self.fields['code'].disabled = True
        if hasattr(self, 'number'):
            self.fields['number'].disabled = True




class CatalogSubtableItemForm(forms.ModelForm):

    dummy = forms.ChoiceField(widget=s2forms.ModelSelect2Widget, required=False)

    def __init__(self, *args, **kwargs):
        super(CatalogSubtableItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            widget.attrs['class'] = 'form-control'
            if isinstance(widget, forms.widgets.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, s2forms.ModelSelect2Widget):
                widget.attrs['data-allow-clear'] = 'true'
                widget.attrs['data-placeholder'] = '---'


DocumentForm = CatalogForm
DocumentSubtableItemForm = CatalogSubtableItemForm
