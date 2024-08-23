from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from re import fullmatch

from ....generic_models import Catalog, SubtableItem
from ...enumerations.gender.models import Gender
from ...catalogs.contact_info_type.models import ContactInfoType


def social_insurance_number_validator(number: str | None) -> None:
    """Проверка корректности СНИЛС."""
    if number is None or number.strip() == '':
        return
    if not fullmatch('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9] [0-9][0-9]', number):
        raise ValidationError('Некорректный СНИЛС: не соответствует шаблону "NNN-NNN-NNN NN".')
    number = number.replace('-', '').replace(' ', '')
    for digit in '0123456789':
        if digit * 3 in number[:-2]:
            raise ValidationError('Некорректный СНИЛС: три одинаковые цифры подряд.')
    control_number = int(number[-2:])
    digits_weighted_sum = sum(int(number[index]) * (9 - index) for index in range(len(number) - 2))
    if digits_weighted_sum % 101 % 100 != control_number:
        raise ValidationError('Некорректный СНИЛС: проверка по контрольным цифрам не пройдена.')


class Individual(Catalog):
    """Физическое лицо."""

    entity_name = 'individual'
    """Внутреннее имя сущности."""

    last_name = models.CharField(_('Фамилия'), max_length=50)
    """Фамилия."""

    first_name = models.CharField(_('Имя'), max_length=50)
    """Имя."""

    patronymic = models.CharField(_('Отчество'), max_length=50, blank=True, default='')
    """Отчество."""

    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, verbose_name='Пол')
    """Пол."""

    birth_date = models.DateField(_('Дата рождения'), blank=True, null=True)
    """Дата рождения."""

    social_insurance_number = models.CharField(
        _('СНИЛС'),
        max_length=14,
        validators=[social_insurance_number_validator],
        blank=True, null=True, unique=True
    )
    """СНИЛС."""

    comment = models.CharField(_('Комментарий'), max_length=255, blank=True, default='')
    """Комментарий."""

    class Meta:
        verbose_name = _("Физическое лицо")
        verbose_name_plural = _("Физические лица")

    @property
    def title_without_status(self):
        result = f'{self.last_name} {self.first_name}'
        if self.patronymic != '':
            result += f' {self.patronymic}'
        return result.strip()

    @property
    def title_with_status(self):
        result = f'{self.last_name} {self.first_name}'
        if self.patronymic != '':
            result += f' {self.patronymic}'
        if hasattr(self, 'rel_student'):
            class_group = self.rel_student.class_group
            if class_group != '':
                result += f' ({class_group})'
        if hasattr(self, 'rel_employee'):
            main_position = self.rel_employee.main_position
            if main_position != '':
                result += f' ({main_position})'
        return result.strip()

    def __str__(self):
        return f'{self.title_without_status}'


class ContactInfoItem(SubtableItem):
    """Единица контактной информации."""

    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, verbose_name='Физическое лицо')
    """Физическое лицо."""

    contact_info_type = models.ForeignKey(ContactInfoType, on_delete=models.RESTRICT, verbose_name='Тип')
    """Тип."""

    value = models.CharField(_("Значение"), max_length=255)
    """Значение."""

    comment = models.CharField(_('Комментарий'), max_length=255, blank=True, null=True, default='')
    """Комментарий."""

    class Meta:
        verbose_name = _("Элемент контактной информации")
        verbose_name_plural = _("Элементы контактной информации")

    def __str__(self):
        return f'{self.individual.title_without_status}: {self.contact_info_type} - {self.value}'
