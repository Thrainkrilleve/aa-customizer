from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AaCustomizerConfig(AppConfig):
    name = "aa_customizer"
    label = "aa_customizer"
    verbose_name = _("AA Customizer")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        pass
