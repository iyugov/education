from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from datetime import datetime


class Catalog(models.Model):
    """Справочник."""

    entity_name = '<catalog>'
    """Внутреннее имя сущности."""

    code = models.IntegerField(_("Код"), unique=True)

    title = models.CharField(_("Наименование"), max_length=50, blank=True, default='')
    """Наименование."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            last_code = self.__class__.objects.all().aggregate(largest=Max('code'))
            if last_code["largest"] is not None:
                self.code = last_code["largest"] + 1
            else:
                self.code = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Document(models.Model):
    """Документ."""

    entity_name = '<document>'
    """Внутреннее имя сущности."""

    number = models.IntegerField(_("Номер"), unique=True)

    date = models.DateField(_("Дата"), default=now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            last_number = self.__class__.objects.all().aggregate(largest=Max('number'))
            if last_number["largest"] is not None:
                self.number = last_number["largest"] + 1
            else:
                self.number = 1
            self.date = datetime.now()
        super().save(*args, **kwargs)


class Enumeration(models.Model):
    """Перечисление."""
    class Meta:
        abstract = True


class RegistryItem(models.Model):
    """Элемент регистра."""
    class Meta:
        abstract = True


class SubtableItem(models.Model):
    """Элемент табличной части."""
    class Meta:
        abstract = True
