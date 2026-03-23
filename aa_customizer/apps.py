import os

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AaCustomizerConfig(AppConfig):
    name = "aa_customizer"
    label = "aa_customizer"
    verbose_name = _("AA Customizer")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        # Alliance Auth requires 'allianceauth' to be first in INSTALLED_APPS
        # (for Django admin favicon support), which means Django's app_directories
        # loader finds allianceauth's templates before ours.  Inserting our
        # templates directory at the end of TEMPLATES[*]['DIRS'] puts it in the
        # filesystem loader chain, which runs before app_directories.  This lets
        # our overrides of allianceauth/* templates (base-bs5.html, overview.html,
        # etc.) take effect while still respecting any project-level DIRS entries
        # that the user has configured (those stay at index 0 and keep priority).
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        from django.conf import settings

        for engine in settings.TEMPLATES:
            if engine.get("BACKEND") == "django.template.backends.django.DjangoTemplates":
                dirs = engine.setdefault("DIRS", [])
                if templates_dir not in dirs:
                    dirs.append(templates_dir)
