from django.db import models
from django.utils.translation import gettext_lazy as _


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
