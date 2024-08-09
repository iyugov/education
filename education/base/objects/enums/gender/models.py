from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.Model):
    """Пол."""

    title = models.CharField(_("Наименование"), max_length=10, unique=True)
    """Наименование."""

    class Meta:
        verbose_name = _("Значение пола")
        verbose_name_plural = _("Значения пола")

    def __str__(self):
        return f'{self.title}'
