from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClassesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classes'
    verbose_name = _("Обучение")
