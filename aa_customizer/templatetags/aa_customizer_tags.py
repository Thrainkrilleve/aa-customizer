"""
Template tags for the aa_customizer app.
"""

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from ..models import CustomBranding

register = template.Library()


def _get_branding(context) -> CustomBranding:
    """Return the branding object from context or the DB."""
    return context.get("AA_CUSTOMIZER") or CustomBranding.get_solo()


# ---------------------------------------------------------------------------
# Favicon / icons
# ---------------------------------------------------------------------------


@register.simple_tag(takes_context=True)
def customizer_favicon_tags(context) -> str:
    """
    Output ``<link>`` tags for a custom favicon.
    Returns an empty string when no favicon is configured so the default AA
    icons.html fallback is used instead.
    """
    branding = _get_branding(context)
    url = branding.effective_favicon

    if not url:
        return ""

    safe_url = conditional_escape(url)
    return mark_safe(
        f'<link rel="apple-touch-icon" sizes="180x180" href="{safe_url}">\n'
        f'<link rel="icon" type="image/png" href="{safe_url}" sizes="192x192">\n'
        f'<link rel="icon" type="image/png" href="{safe_url}" sizes="96x96">\n'
        f'<link rel="icon" type="image/png" href="{safe_url}" sizes="32x32">\n'
        f'<link rel="icon" type="image/png" href="{safe_url}" sizes="16x16">\n'
        f'<link rel="shortcut icon" href="{safe_url}">\n'
    )


# ---------------------------------------------------------------------------
# Login page helpers
# ---------------------------------------------------------------------------


@register.inclusion_tag(
    "aa_customizer/partials/login_branding.html", takes_context=True
)
def customizer_login_branding(context):
    """
    Render the optional logo, title, and subtitle block at the top of the login card.
    Checks both URL fields and uploaded files via the model's effective_* properties.
    """
    branding = _get_branding(context)
    return {
        "branding": branding,
        "has_branding": bool(
            branding.effective_login_logo
            or branding.login_title
            or branding.login_subtitle
        ),
    }


# ---------------------------------------------------------------------------
# Navbar logo
# ---------------------------------------------------------------------------


@register.inclusion_tag(
    "aa_customizer/partials/navbar_logo.html", takes_context=True
)
def customizer_navbar_logo(context):
    """
    Render the optional navbar logo ``<img>`` element.
    Checks both URL and uploaded file via the model's effective_navbar_logo property.
    """
    branding = _get_branding(context)
    return {
        "branding": branding,
        "site_name": context.get("SITE_NAME", ""),
    }


# ---------------------------------------------------------------------------
# Utility — branding access in templates without the context processor
# ---------------------------------------------------------------------------


@register.simple_tag()
def superuser_branding() -> CustomBranding:
    """
    Return the CustomBranding singleton for use in templates that are rendered
    via inclusion tags (e.g. ``{% status_overview %}``) where the context
    processor does not run and ``AA_CUSTOMIZER`` is not available.
    """
    return CustomBranding.get_solo()


@register.simple_tag()
def get_branding() -> CustomBranding:
    """
    Generic alias for ``superuser_branding``.  Use this in any third-party
    widget or plugin template to access the CustomBranding singleton without
    depending on the context processor being in scope.

    Example::

        {% load aa_customizer_tags %}
        {% get_branding as branding %}
        {% if branding.custom_css %}...{% endif %}
    """
    return CustomBranding.get_solo()

