from django.db import models
from django.utils.translation import gettext_lazy as _

from ....generic_models import Catalog
from ...catalogs.individual.models import Individual


class Student(Catalog):
    """Ученик (физическое лицо)."""

    entity_name = 'student'
    """Внутреннее имя сущности."""

    individual = models.OneToOneField(Individual, on_delete=models.RESTRICT, related_name='rel_student', verbose_name='Физическое лицо')
    """Физическое лицо."""

    class Meta:
        verbose_name = _('Обучающийся')
        verbose_name_plural = _('Обучающиеся')

    @property
    def title_without_status(self):
        return f'{self}'

    @property
    def class_group(self):
        if hasattr(self, 'class_group_enrollment_registry'):
            last_class_group_enrollment = self.class_group_enrollment_registry.order_by('-enrollment_date').first()
            if last_class_group_enrollment:
                return last_class_group_enrollment.class_group
        return ''

    @property
    def title_with_status(self):
        class_group = self.class_group
        if class_group != '':
            return f'{self.title_without_status} ({class_group})'
        else:
            return f'{self.title_without_status}'

    def __str__(self):
        return f'{self.individual}'
