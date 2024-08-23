from django import forms
from django_select2 import forms as s2forms
from ....generic_forms import DocumentForm, DocumentSubtableItemForm

from ....entities.documents.pass_tag_request.models import PassTagRequest, PassTagRequestItem

from ....entities.catalogs.individual.models import Individual
from ....entities.catalogs.pass_tag.models import PassTag


class IndividualWidget(s2forms.ModelSelect2Widget):

    search_fields = [
        "last_name__icontains",
        "first_name__icontains",
        "patronymic__icontains",
    ]

    queryset = Individual.objects.all().order_by('last_name', 'first_name', 'patronymic')

    @staticmethod
    def label_from_instance(object_to_select):
        return object_to_select.title_with_status


class PassTagRequestItemForm(DocumentSubtableItemForm):
    class Meta:
        model = PassTagRequestItem
        fields = ['pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status']
        widgets = {
            'holder': IndividualWidget,
            'pass_tag': s2forms.ModelSelect2Widget(
                search_fields=["tag_id__icontains"],
                queryset=PassTag.objects.all().order_by('tag_id')
            ),
        }


class PassTagRequestForm(DocumentForm):
    class Meta:
        model = PassTagRequest
        fields = ['number', 'date', 'requester', 'executor', 'request_date', 'comment']
        widgets = {
            'requester': IndividualWidget,
            'executor': IndividualWidget,
        }

    pass_tag_request_item_list = forms.inlineformset_factory(
        PassTagRequest,
        PassTagRequestItem,
        form=PassTagRequestItemForm,
        extra=1,
        can_delete=True
    )
