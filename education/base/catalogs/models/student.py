from django.db import models
from django.utils.translation import gettext_lazy as _

from .individual import Individual


class Student(models.Model):
    """Ученик (физическое лицо)."""

    individual = models.OneToOneField(Individual, on_delete=models.RESTRICT, related_name='rel_student', verbose_name='Физическое лицо')
    """Физическое лицо."""

    class Meta:
        verbose_name = _('Обучающийся')
        verbose_name_plural = _('Обучающиеся')

    @property
    def title_without_status(self):
        return f'{self.individual.title_without_status}'

    @property
    def class_group(self):
        last_class_group_enrollment = self.class_group_enrollment_registry.order_by('-enrollment_date').first()
        if last_class_group_enrollment:
            return f'{last_class_group_enrollment.class_group}'
        else:
            return ''

    @property
    def title_with_status(self):
        last_class_group_enrollment_registry_item = self.class_group_enrollment_registry.order_by('-enrollment_date').first()
        if last_class_group_enrollment_registry_item:
            return f'{self.individual.title_without_status} ({last_class_group_enrollment_registry_item.class_group})'
        else:
            return f'{self.individual.title_without_status}'

    def __str__(self):
        return f'{self.title_without_status}'
