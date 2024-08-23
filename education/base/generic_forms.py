from django import forms
from django_select2 import forms as s2forms


class BasicEntityForm(forms.ModelForm):

    dummy = forms.ChoiceField(widget=s2forms.ModelSelect2Widget, required=False)

    def __init__(self, *args, **kwargs):
        super(BasicEntityForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if isinstance(visible.field.widget, forms.widgets.CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(visible.field.widget, s2forms.ModelSelect2Widget):
                visible.field.widget.attrs['data-allow-clear'] = 'true'
                visible.field.widget.attrs['data-placeholder'] = '---'


class CatalogForm(BasicEntityForm):

    def __init__(self, *args, **kwargs):
        super(CatalogForm, self).__init__(*args, **kwargs)
        if 'code' in self.fields:
            self.fields['code'].widget.attrs['readonly'] = True


class DocumentForm(BasicEntityForm):

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        if 'number' in self.fields:
            self.fields['number'].widget.attrs['readonly'] = True


class BasicSubtableItemForm(forms.ModelForm):

    dummy = forms.ChoiceField(widget=s2forms.ModelSelect2Widget, required=False)

    def __init__(self, *args, **kwargs):
        super(BasicSubtableItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            widget.attrs['class'] = 'form-control'
            if isinstance(widget, forms.widgets.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, s2forms.ModelSelect2Widget):
                widget.attrs['data-allow-clear'] = 'true'
                widget.attrs['data-placeholder'] = '---'


class CatalogSubtableItemForm(BasicSubtableItemForm):
    pass


class DocumentSubtableItemForm(BasicSubtableItemForm):
    pass
