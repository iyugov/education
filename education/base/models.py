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
        return
    number = number.replace('-', '').replace(' ', '')
    for digit in '0123456789':
        if digit * 3 in number:
            raise ValidationError('Некорректный СНИЛС: три одинаковые цифры подряд.')
            return
    control_number = int(number[-2:])
    digits_weighted_sum = sum(int(number[index]) * (9 - index) for index in range(len(number) - 2))
    if digits_weighted_sum % 101 != control_number:
        raise ValidationError('Некорректный СНИЛС: проверка по контрольным цифрам не пройдена.')

# Create your models here.

class Individual(models.Model):
    '''Физическое лицо.'''
    
    GENDER_CHOICES = [
        ('Ж', 'Женский'),
        ('M', 'Мужской'),
        ('-', 'Не указан'),
    ]
    '''Пол (значения).'''

    last_name = models.CharField(_("Фамилия"), max_length=50)
    '''Фамилия.'''
   
    first_name = models.CharField(_("Имя"), max_length=50)
    '''Имя.'''
   
    patronymic = models.CharField(_("Отчество"), max_length=50, blank=True, null=True)
    '''Отчество.'''
    
    gender = models.CharField(_("Пол"), max_length=1, choices=GENDER_CHOICES, default='-')
    '''Пол.'''
    
    birth_date = models.DateField(_("Дата рождения"), blank=True, null=True)
    '''Дата рождения.'''

    social_insurance_number = models.CharField(
        _("СНИЛС"),
        max_length=14, 
        validators=[social_insurance_number_validator],
       blank=True, null=True, unique=True
    )
    '''СНИЛС.'''
    
    is_student = models.BooleanField(_("Обучающийся"), default=False)
    '''Является ли обучающимся.'''
       
    class Meta:
        verbose_name = _("Физическое лицо")
        verbose_name_plural = _("Физические лица")

    def __str__(self):
       result = f'{self.last_name} {self.first_name}'
       if self.patronymic != '':
           result += f' {self.patronymic}'
       return result.strip()
