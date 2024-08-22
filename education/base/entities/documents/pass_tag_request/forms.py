from django import forms

from ....entities.documents.pass_tag_request.models import PassTagRequest, PassTagRequestItem
from ....entities.catalogs.individual.models import Individual


class IndividualModelChoiceField(forms.ModelChoiceField):

    individual_cache = {instance: instance.title_with_status for instance in Individual.objects.all()}

    def label_from_instance(self, object_to_select):
        return self.individual_cache[object_to_select]


class PassTagRequestItemForm(forms.ModelForm):
    class Meta:
        model = PassTagRequestItem
        fields = ['pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status']

    holder = IndividualModelChoiceField(queryset=Individual.objects.all(), label='Держатель')

    def __init__(self, *args, **kwargs):
        super(PassTagRequestItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'


class PassTagRequestForm(forms.ModelForm):
    class Meta:
        model = PassTagRequest
        fields = ['number', 'date', 'requester', 'executor', 'request_date', 'comment']

    pass_tag_request_item_list = forms.inlineformset_factory(
        PassTagRequest,
        PassTagRequestItem,
        form=PassTagRequestItemForm,
        extra=1,
        can_delete=True
    )

    individual_cache = Individual.objects.all()

    requester = IndividualModelChoiceField(queryset=individual_cache, label='Заявитель')
    executor = IndividualModelChoiceField(queryset=individual_cache, label='Исполнитель')

    def __init__(self, *args, **kwargs):
        super(PassTagRequestForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['number'].disabled = True

