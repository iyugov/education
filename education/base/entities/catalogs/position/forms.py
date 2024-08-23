from ....generic_forms import CatalogForm

from ....entities.catalogs.position.models import Position


class PositionForm(CatalogForm):

    class Meta:
        model = Position
        fields = ['code', 'title']
