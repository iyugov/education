from django import forms
from ....generic_forms import CatalogForm

from ....entities.catalogs.transport_pass.models import TransportPass


class TransportPassForm(CatalogForm):
    class Meta:
        model = TransportPass
        fields = ['code', 'pass_id']
