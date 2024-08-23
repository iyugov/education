from django.db import models
from django.utils.translation import gettext_lazy as _
from re import fullmatch
from django.core.validators import ValidationError

from ....generic_models import Catalog


def pass_id_validator(pass_id: str | None) -> None:
    """Проверка корректности идентификатора карты."""
    if pass_id is None or not fullmatch('[0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9] [0-9][0-9][0-9]', pass_id):
        raise ValidationError('Некорректный номер: не соответствует шаблону "NNNN NNNN NNN".')


class TransportPass(Catalog):
    """Транспортная карта."""

    entity_name = 'transport_pass'
    """Внутреннее имя сущности."""

    pass_id = models.CharField(_('Номер'), validators=[pass_id_validator], max_length=13, unique=True)
    """Идентификатор."""
    
    class Meta:
        verbose_name = _('Транспортная карта')
        verbose_name_plural = _('Транспортные карты')

    def __str__(self):
        return self.pass_id
