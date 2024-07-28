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


class PassCardType(models.Model):
    """Тип пропускной карты."""

    title = models.CharField(_('Наименование'), max_length=50, unique=True)
    '''Наименование.'''
       
    class Meta:
        verbose_name = _('Тип пропускных карт')
        verbose_name_plural = _('Типы пропускных карт')

    def __str__(self):
        return self.title


class PassCardAction(models.Model):
    """Тип пропускной карты."""

    title = models.CharField(_('Наименование'), max_length=50, unique=True)
    '''Наименование.'''
       
    class Meta:
        verbose_name = _('Действие с картами')
        verbose_name_plural = _('Действие с картами')

    def __str__(self):
        return self.title


class PassCard(models.Model):
    """Пропускная карта."""

    pass_id = models.CharField(_('Идентификатор'), validators=[pass_id_validator], max_length=9)
    '''Идентификатор.'''

    pass_type = models.ForeignKey(PassCardType, null=True, on_delete=models.RESTRICT, verbose_name='Тип')
    '''Тип.'''
    
    class Meta:
        verbose_name = _('Пропускная карта')
        verbose_name_plural = _('Пропускные карты')

    def __str__(self):
        return self.pass_id


class PassCardIssue(models.Model):
    """Оформление карты."""

    issue_date = models.DateField(_('Дата оформления'), default=now)
    '''Дата рождения.'''

    card = models.ForeignKey(PassCard, null=True, on_delete=models.RESTRICT, verbose_name='Карта')
    '''Карта.'''

    individual = models.ForeignKey(Individual, null=True, on_delete=models.PROTECT, verbose_name='Физическое лицо')
    '''Физическое лицо.'''
    
    description = models.CharField(_('Описание'), max_length=30, default='')
    '''Описание физического лица.'''
    
    action = models.ForeignKey(PassCardAction, null=True, on_delete=models.PROTECT, verbose_name='Действие')
    '''Действие.'''

    class Meta:
        verbose_name = _('Оформление карты')
        verbose_name_plural = _('Оформление карт')

    def __str__(self):
        return f'{self.issue_date:%d.%m.%Y}: {self.individual} ({self.card})'
