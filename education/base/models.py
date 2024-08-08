from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError
from re import fullmatch


def social_insurance_number_validator(number: str | None) -> None:
    """Проверка корректности СНИЛС."""
    if number is None or number.strip() == '':
        return
    if not fullmatch('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9] [0-9][0-9]', number):
        raise ValidationError('Некорректный СНИЛС: не соответствует шаблону "NNN-NNN-NNN NN".')
    number = number.replace('-', '').replace(' ', '')
    for digit in '0123456789':
        if digit * 3 in number:
            raise ValidationError('Некорректный СНИЛС: три одинаковые цифры подряд.')
    control_number = int(number[-2:])
    digits_weighted_sum = sum(int(number[index]) * (9 - index) for index in range(len(number) - 2))
    if digits_weighted_sum % 101 != control_number:
        raise ValidationError('Некорректный СНИЛС: проверка по контрольным цифрам не пройдена.')


# Create your models here.

class Gender(models.Model):
    """Пол."""

    title = models.CharField(_("Наименование"), max_length=10, unique=True)
    """Наименование."""

    class Meta:
        verbose_name = _("Значение пола")
        verbose_name_plural = _("Значения пола")

    def __str__(self):
        return f'{self.title}'


class Individual(models.Model):
    """Физическое лицо."""

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
        if hasattr(self, 'student'):
            last_class_group_enrollment_registry_item = self.student.class_group_enrollment_registry.order_by('-enrollment_date').first()
            if last_class_group_enrollment_registry_item:
                result += f' ({last_class_group_enrollment_registry_item.class_group})'
        return result.strip()

    def __str__(self):
        return f'{self.title_with_status}'


class ContactInfoType(models.Model):
    """Тип контактной информации."""

    title = models.CharField(_("Наименование"), max_length=50, unique=True)
    """Наименование."""

    class Meta:
        verbose_name = _("Тип контактной информации")
        verbose_name_plural = _("Типы контактной информации")

    def __str__(self):
        return self.title


class ContactInfoItem(models.Model):
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

