from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from ....generic_models import Document, SubtableItem
from ....entities.catalogs.student.models import Student
from ....entities.catalogs.class_group.models import ClassGroup


class ClassGroupEnrollment(Document):
    """Зачисление обучающихся в классы."""

    entity_name = 'class_group_enrollment'
    """Внутреннее имя сущности."""

    enrollment_date = models.DateField(_('Дата зачисления'), default=now)
    """Дата зачисления."""

    class Meta:
        verbose_name = _("Зачисление обучающихся в классы")
        verbose_name_plural = _("Зачисления обучающихся в классы")

    @property
    def presentation(self):
        return f'{self}'

    def __str__(self):
        return f'№{self.pk} от {self.enrollment_date:%d.%m.%Y}'


class ClassGroupEnrollmentItem(SubtableItem):
    """Элемент зачисления в класс."""

    class_group_enrollment = models.ForeignKey(ClassGroupEnrollment, null=True, on_delete=models.CASCADE, verbose_name='Зачисление')
    """Зачисление."""

    student = models.ForeignKey(Student, null=True, on_delete=models.RESTRICT, verbose_name='Обучающийся')
    """Обучающийся."""

    class_group = models.ForeignKey(ClassGroup, null=True, on_delete=models.PROTECT, verbose_name='Класс')
    """Класс."""

    class Meta:
        verbose_name = _("Элемент зачисления в класс")
        verbose_name_plural = _("Элементы зачисления в класс")

    def __str__(self):
        return f'{self.student.title_without_status} -> {self.class_group}'
