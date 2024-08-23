from ....generic_forms import CatalogForm

from ....entities.catalogs.contact_info_type.models import ContactInfoType


class ContactInfoTypeForm(CatalogForm):
    class Meta:
        model = ContactInfoType
        fields = ['code', 'title']

