from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from ....objects.catalogs.student.models import Student
from ....objects.catalogs.class_group.models import ClassGroup
from ....objects.documents.class_group_enrollment.models import ClassGroupEnrollment


class ClassGroupEnrollmentRegistryItem(models.Model):
    """Элемент зачисления в класс."""

    is_registry = True
    """Является ли регистром."""

    class_group_enrollment = models.ForeignKey(ClassGroupEnrollment, null=True, on_delete=models.CASCADE, verbose_name='Зачисление')
    """Зачисление."""

    enrollment_date = models.DateField(_('Дата зачисления'), default=now)
    """Дата зачисления."""

    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, verbose_name='Обучающийся', related_name='class_group_enrollment_registry')
    """Обучающийся."""

    class_group = models.ForeignKey(ClassGroup, null=True, on_delete=models.CASCADE, verbose_name='Класс')
    """Класс."""

    class Meta:
        verbose_name = _("Элемент зачисления в класс (регистр)")
        verbose_name_plural = _("Элементы зачисления в класс (регистр)")

    def __str__(self):
        return f'{self.class_group_enrollment}: {self.student} -> {self.class_group}'