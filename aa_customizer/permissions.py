"""
Permission helpers for aa_customizer admin views.

Separated from admin.py so they can be imported in tests without triggering
the Django admin registry (which requires ``django.contrib.admin`` in
``INSTALLED_APPS``).
"""

from django.conf import settings


def _is_trusted_admin(request):
    """
    Return True if the requesting user is allowed to view or modify
    CustomBranding settings.

    When ``AA_CUSTOMIZER_TRUSTED_USER_IDS`` is set in Django settings (i.e.
    ``local.py``) to a non-empty list of integer user PKs, *only* those users
    are granted access — regardless of superuser status.  This limits the
    blast radius of a privilege-escalation exploit: an attacker who grants
    themselves ``is_superuser`` via a DB exploit still cannot reach the
    branding fields unless their PK appears in the server-side ``local.py``
    whitelist.

    When the setting is absent or empty, access falls back to any superuser
    (preserving backward-compatible behaviour for existing deployments).

    Example ``local.py`` entry::

        AA_CUSTOMIZER_TRUSTED_USER_IDS = [1, 7]
    """
    trusted = getattr(settings, "AA_CUSTOMIZER_TRUSTED_USER_IDS", [])
    if trusted:
        return request.user.pk in trusted
    return request.user.is_superuser
