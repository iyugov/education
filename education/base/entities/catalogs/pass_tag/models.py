from django.db import models
from django.utils.translation import gettext_lazy as _
from re import fullmatch
from django.core.validators import ValidationError

from ....generic_models import Catalog


def tag_id_validator(pass_id: str | None) -> None:
    """Проверка корректности идентификатора чипа."""
    if pass_id is None or not fullmatch('[0-9][0-9][0-9],[0-9][0-9][0-9][0-9][0-9]', pass_id):
        raise ValidationError('Некорректный идентификатор: не соответствует шаблону "NNN,NNNNN".')
    pass_id_parts = tuple(map(int, pass_id.split(',')))
    if pass_id_parts[0] > 255 or pass_id_parts[1] > 65535:
        raise ValidationError('Некорректный идентификатор: числовое значение вне допустимого диапазона.')


class PassTag(Catalog):
    """Чип."""

    entity_name = 'pass_tag'
    """Внутреннее имя сущности."""

    tag_id = models.CharField(_('Идентификатор'), validators=[tag_id_validator], max_length=9, unique=True)
    """Идентификатор."""
    
    class Meta:
        verbose_name = _('Чип')
        verbose_name_plural = _('Чипы')

    def __str__(self):
        return self.tag_id
