from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from re import fullmatch
from base.models import Individual
from django.utils.timezone import now

# Create your models here.


def pass_id_validator(pass_id: str | None) -> None:
    """Проверка корректности идентификатора карты."""
    if pass_id is None or not fullmatch('[0-9][0-9][0-9],[0-9][0-9][0-9][0-9][0-9]', pass_id):
        raise ValidationError('Некорректный идентификатор: не соответствует шаблону "NNN,NNNNN".')
    pass_id_parts = tuple(map(int, pass_id.split(',')))
    if pass_id_parts[0] > 255 or pass_id_parts[1] > 65535:
        raise ValidationError('Некорректный идентификатор: числовое значение вне допустимого диапазона.')


class PassTag(models.Model):
    """Чип."""

    tag_id = models.CharField(_('Идентификатор'), validators=[pass_id_validator], max_length=9, unique=True)
    """Идентификатор."""
    
    class Meta:
        verbose_name = _('Чип')
        verbose_name_plural = _('Чипы')

    def __str__(self):
        return self.tag_id


class PassTagRequest(models.Model):
    """Заявка на чипы."""

    requester = models.ForeignKey(Individual, null=True, on_delete=models.PROTECT, related_name='requester', verbose_name='Заявитель')
    """Заявитель (физическое лицо)."""

    executor = models.ForeignKey(Individual, null=True, on_delete=models.PROTECT, related_name='executor', verbose_name='Исполнитель')
    """Исполнитель (физическое лицо)."""

    request_date = models.DateField(_('Дата заявки'), default=now)
    """Дата заявки."""

    comment = models.CharField(_('Комментарий'), max_length=255, blank=True, default='')
    """Комментарий."""

    class Meta:
        verbose_name = _('Заявка на чипы')
        verbose_name_plural = _('Заявки на чипы')

    def __str__(self):
        return f'{self.request_date:%d.%m.%Y}'
