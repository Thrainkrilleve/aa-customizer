"""
Context processor for the aa_customizer app.

Adds the ``AA_CUSTOMIZER`` branding object and optionally overrides
``SITE_NAME`` in every template context.
"""

from django.conf import settings as django_settings

from .models import CustomBranding


def aa_customizer(request):
    """
    Inject branding settings into every template context.

    ``AA_CUSTOMIZER`` — the :class:`CustomBranding` singleton instance.
    ``SITE_NAME``     — overridden with the custom value when one is set;
                        otherwise falls back to ``settings.SITE_NAME``.
    """
    branding = CustomBranding.get_solo()
    return {
        "AA_CUSTOMIZER": branding,
        "SITE_NAME": branding.site_name or getattr(django_settings, "SITE_NAME", "Alliance Auth"),
    }
