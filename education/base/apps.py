from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    verbose_name = _("Основное")

    def ready(self):
        post_migrate.connect(create_objects, sender=self)


def create_objects(sender, **kwargs):
    from .entities.enumerations.gender.models import Gender
    for title in ('Не указан', 'Женский', 'Мужской'):
        if not Gender.objects.filter(title=title).exists():
            Gender.objects.create(title=title)
