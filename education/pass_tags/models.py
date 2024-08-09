from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from re import fullmatch
from base.catalogs.models.individual import Individual
from django.utils.timezone import now

# Create your models here.


def tag_id_validator(pass_id: str | None) -> None:
    """Проверка корректности идентификатора карты."""
    if pass_id is None or not fullmatch('[0-9][0-9][0-9],[0-9][0-9][0-9][0-9][0-9]', pass_id):
        raise ValidationError('Некорректный идентификатор: не соответствует шаблону "NNN,NNNNN".')
    pass_id_parts = tuple(map(int, pass_id.split(',')))
    if pass_id_parts[0] > 255 or pass_id_parts[1] > 65535:
        raise ValidationError('Некорректный идентификатор: числовое значение вне допустимого диапазона.')


class PassTag(models.Model):
    """Чип."""

    tag_id = models.CharField(_('Идентификатор'), validators=[tag_id_validator], max_length=9, unique=True)
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

    @property
    def presentation(self):
        return f'{self}'

    def __str__(self):
        return f'№{self.pk} от {self.request_date:%d.%m.%Y}'


class PassTagRequestItem(models.Model):
    """Элемент заявки на чипы."""

    REASON_INITIAL_PRIMARY = 'Первоначальный'
    REASON_REPLACE_LOST = 'Замена утраченного'
    REASON_REPLACE_DAMAGED = 'Замена испорченного'
    REASON_INITIAL_SECONDARY = 'Дополнительный'
    REASON_NOT_SPECIFIED = 'Не указано'
    REASON_CHOICES = [
        (REASON_INITIAL_PRIMARY, REASON_INITIAL_PRIMARY),
        (REASON_REPLACE_LOST, REASON_REPLACE_LOST),
        (REASON_REPLACE_DAMAGED, REASON_REPLACE_DAMAGED),
        (REASON_INITIAL_SECONDARY, REASON_INITIAL_SECONDARY),
        (REASON_NOT_SPECIFIED, REASON_NOT_SPECIFIED),
    ]
    """Причина заявки (значения)."""

    STATUS_REQUEST = 'Заявка'
    STATUS_IN_PROGRESS = 'В работе'
    STATUS_DECLINED = 'Отклонено'
    STATUS_COMPLETED = 'Выполнено'
    STATUS_CHOICES = [
        (STATUS_REQUEST, STATUS_REQUEST),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS),
        (STATUS_DECLINED, STATUS_DECLINED),
        (STATUS_COMPLETED, STATUS_COMPLETED),
    ]
    """Статус обработки (значения)."""

    pass_tag_request = models.ForeignKey(PassTagRequest, on_delete=models.CASCADE, verbose_name='Заявка')
    """Заявка."""

    holder = models.ForeignKey(Individual, null=True, on_delete=models.PROTECT, verbose_name='Держатель')
    """Держатель чипа (физическое лицо)."""

    reason = models.CharField(_('Причина'), max_length=50, choices=REASON_CHOICES, default=REASON_NOT_SPECIFIED)
    """Причина."""

    processing_date = models.DateField(_('Дата обработки'), blank=True, null=True, default=now)
    """Дата обработки."""

    pass_tag = models.ForeignKey(PassTag, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Чип')
    """Чип."""

    status = models.CharField(_('Статус'), max_length=50, choices=STATUS_CHOICES, default=STATUS_REQUEST)
    """Статус."""

    class Meta:
        verbose_name = _('Элемент заявки на чипы')
        verbose_name_plural = _('Элементы заявки на чипы')

    def __str__(self):
        return f'{self.pass_tag_request}: {self.processing_date:%d.%m.%Y}, {self.holder}, {self.reason} [{self.status}]'