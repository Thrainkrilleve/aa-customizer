"""
Admin configuration for the aa_customizer app.
"""

from solo.admin import SingletonModelAdmin

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import CustomBrandingAdminForm
from .models import CustomBranding


@admin.register(CustomBranding)
class CustomBrandingAdmin(SingletonModelAdmin):
    """
    Admin interface for the CustomBranding singleton.
    Each image element provides a URL field (recommended for Docker) and a file
    upload field — set whichever suits your environment.  URL always wins.
    """

    form = CustomBrandingAdminForm
    save_on_top = True

    fieldsets = (
        (
            _("Site"),
            {
                "fields": ("site_name",),
                "description": _(
                    "Override the site name shown in the browser title bar, navbar, and "
                    "login page. Leave blank to keep the value from local.py."
                ),
            },
        ),
        (
            _("Login Page — Background"),
            {
                "fields": (
                    "login_background_url",
                    "login_background",
                    "login_background_color",
                ),
                "description": _(
                    "Set a background for the login page. "
                    "Priority: URL → uploaded file → color. "
                    "Leave everything blank to use the default Alliance Auth space background."
                ),
            },
        ),
        (
            _("Login Page — Branding"),
            {
                "fields": (
                    "login_logo_url",
                    "login_logo",
                    "login_logo_max_width",
                    "login_title",
                    "login_subtitle",
                    "login_extra_html",
                ),
                "description": _(
                    "Optional logo, heading, description, and extra HTML shown on the login card. "
                    "For each image, a URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Favicon"),
            {
                "fields": ("favicon_url", "favicon"),
                "description": _(
                    "Replace the Alliance Auth favicon. URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Navigation Bar Logo"),
            {
                "fields": ("navbar_logo_url", "navbar_logo", "navbar_logo_height"),
                "description": _(
                    "Optional logo displayed next to the site name in the navbar. "
                    "URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Sidebar Logo"),
            {
                "fields": ("sidebar_logo_url", "sidebar_logo", "sidebar_logo_width"),
                "description": _(
                    "Replaces the Alliance Auth logo at the bottom of the sidebar. "
                    "URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Custom CSS"),
            {
                "fields": ("custom_css_url", "custom_css"),
                "description": _(
                    "Inject additional CSS into every page. "
                    "The linked stylesheet (URL) is loaded first; the inline block is applied after it. "
                    "Both are loaded after the active AA theme so they override any existing style. "
                    "Works alongside Alliance Auth's built-in Custom CSS admin."
                ),
            },
        ),
        (
            _("Extra HTML"),
            {
                "fields": ("head_extra_html",),
                "description": _(
                    "Raw HTML injected at the end of <head> on every page. "
                    "Useful for analytics snippets, Google Fonts imports, or custom meta tags. "
                    "Contents are not sanitized — only admins should edit this field."
                ),
            },
        ),
    )
