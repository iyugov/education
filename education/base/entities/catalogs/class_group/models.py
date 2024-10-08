from django.db import models
from django.utils.translation import gettext_lazy as _

from ....generic_models import Catalog


class ClassGroup(Catalog):
    """Класс (группа обучающихся)."""

    entity_name = 'class_group'
    """Внутреннее имя сущности."""

    grade = models.IntegerField(_("Параллель"), default=0)
    """Параллель."""

    label = models.CharField(_("Литера"), max_length=1, default='', blank=True)
    """Литера."""

    class Meta:
        verbose_name = _("Класс")
        verbose_name_plural = _("Классы")

    @property
    def presentation(self):
        return f'{self}'

    def __str__(self):
        if self.label in (x for x in '0123456789'):
            return f'{self.grade}-{self.label}'
        else:
            return f'{self.grade}{self.label}'

