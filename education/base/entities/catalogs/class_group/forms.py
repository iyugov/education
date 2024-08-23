from ....generic_forms import CatalogForm

from ....entities.catalogs.class_group.models import ClassGroup


class ClassGroupForm(CatalogForm):

    class Meta:
        model = ClassGroup
        fields = ['code', 'grade', 'label']
