from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PassCardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pass_tags'
    verbose_name = _("Чипы")
