from django.db import models
from django.utils.translation import gettext_lazy as _

from ....generic_models import Catalog


class Position(Catalog):
    """Ученик (физическое лицо)."""

    entity_name = 'position'
    """Внутреннее имя сущности."""

    class Meta:
        verbose_name = _('Должность')
        verbose_name_plural = _('Должности')
