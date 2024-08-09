from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactInfoType(models.Model):
    """Тип контактной информации."""

    title = models.CharField(_("Наименование"), max_length=50, unique=True)
    """Наименование."""

    class Meta:
        verbose_name = _("Тип контактной информации")
        verbose_name_plural = _("Типы контактной информации")

    def __str__(self):
        return self.title
