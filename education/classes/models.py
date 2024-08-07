from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import Individual
from django.utils.timezone import now

# Create your models here.


class Student(models.Model):
    """Ученик (физическое лицо)."""

    individual = models.OneToOneField(Individual, on_delete=models.CASCADE, related_name='student', verbose_name='Физическое лицо')
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


class ClassGroup(models.Model):
    """Класс (группа обучающихся)."""
    
    grade = models.IntegerField(_("Параллель"), default=0)
    """Параллель."""
   
    label = models.CharField(_("Литера"), max_length=1, default='', blank=True, null=True)
    """Литера."""
       
    class Meta:
        verbose_name = _("Класс")
        verbose_name_plural = _("Классы")

    @property
    def presentation(self):
        return f'{self}'

    def __str__(self):
        if self.label in (x for x in '0123456789'):
            return f'{self.grade}-{self.label}'
        else:
            return f'{self.grade}{self.label}'


class ClassGroupEnrollment(models.Model):
    """Зачисление обучающихся в классы."""

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

class ClassGroupEnrollmentItem(models.Model):
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