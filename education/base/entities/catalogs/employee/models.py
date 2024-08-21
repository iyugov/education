from django.db import models
from django.utils.translation import gettext_lazy as _

from ....generic_models import Catalog, SubtableItem
from ...catalogs.individual.models import Individual
from ...catalogs.position.models import Position


class Employee(Catalog):
    """Сотрудник (физическое лицо)."""

    entity_name = 'employee'
    """Внутреннее имя сущности."""

    individual = models.OneToOneField(Individual, on_delete=models.RESTRICT, related_name='rel_employee', verbose_name='Физическое лицо')
    """Физическое лицо."""

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')

    @property
    def title_without_status(self):
        return f'{self}'

    @property
    def main_position(self):
        employee_positions = self.positionitem_set
        main_position = employee_positions.filter(is_main=True).first()
        if main_position:
            return f'{main_position.position}'
        else:
            main_position = employee_positions.filter(is_main=False).first()
            if main_position:
                return f'{main_position.position}'
            else:
                return ''

    @property
    def title_with_status(self):
        main_position = self.main_position
        if main_position != '':
            return f'{self.title_without_status} ({main_position})'
        else:
            return f'{self.title_without_status}'

    def __str__(self):
        return f'{self.individual}'


class PositionItem(SubtableItem):
    """Единица списка должностей."""

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Сотрудник')
    """Физическое лицо."""

    position = models.ForeignKey(Position, on_delete=models.RESTRICT, verbose_name='Должность')
    """Тип."""

    is_main = models.BooleanField(_("Основная"))
    """Значение."""

    class Meta:
        verbose_name = _("Элемент списка должностей")
        verbose_name_plural = _("Элементы списка должностей")

    def __str__(self):
        return f'{self.employee.individual.title_without_status}: {self.position}{' (основная)' if self.is_main else ''}'
