from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import Individual
from django.utils.timezone import now

# Create your models here.


class ClassGroup(models.Model):
    """Класс (группа обучающихся)."""
    
    grade = models.IntegerField(_("Параллель"), default=0)
    """Параллель."""
   
    label = models.CharField(_("Литера"), max_length=1, default='', blank=True, null=True)
    """Литера."""
       
    class Meta:
        verbose_name = _("Класс")
        verbose_name_plural = _("Классы")

    def __str__(self):
        if self.label in (x for x in '0123456789'):
            return f'{self.grade}-{self.label}'
        else:
            return f'{self.grade}{self.label}'


class ClassGroupEnrollment(models.Model):
    """Зачисление физического лица (обучающегося) в класс (группу обучающихся)."""

    student = models.ForeignKey(Individual, null=True, on_delete=models.PROTECT, verbose_name='Обучающийся')
    """Физическое лицо (обучающийся)."""

    class_group = models.ForeignKey(ClassGroup, null=True, on_delete=models.PROTECT, verbose_name='Класс')
    """Класс (группа обучающихся)."""

    enrollment_date = models.DateField(_('Дата зачисления'), default=now)
    """Дата рождения."""

    class Meta:
        verbose_name = _("Зачисление обучающегося в класс")
        verbose_name_plural = _("Зачисление обучающегося в класс")

    def __str__(self):
        return f'{self.enrollment_date:%d.%m.%Y}: {self.student} -> {self.class_group}'
