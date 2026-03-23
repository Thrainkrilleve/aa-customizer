"""
Admin configuration for the aa_customizer app.
"""

from solo.admin import SingletonModelAdmin

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import CustomBrandingAdminForm
from .models import AACMediaImage, CustomBranding


@admin.register(AACMediaImage)
class AACMediaImageAdmin(admin.ModelAdmin):
    """
    Admin for the image media library.  Upload images here once, then select
    them from any image slot in Custom Branding without re-uploading.
    """

    list_display = ("name", "image_type", "thumbnail", "uploaded")
    list_filter = ("image_type",)
    search_fields = ("name",)
    readonly_fields = ("thumbnail", "uploaded")
    fields = ("name", "image_type", "image", "thumbnail", "uploaded")

    @admin.display(description=_("Preview"))
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px; max-width:160px; object-fit:contain;">',
                obj.image.url,
            )
        return "—"


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
                    "login_background_library",
                    "login_background",
                    "login_background_color",
                    "login_background_video_loop_count",
                ),
                "description": _(
                    "Set a background for the login page. "
                    "Priority: URL → library selection → uploaded file → color. "
                    "Leave everything blank to use the default Alliance Auth space background. "
                    "Loop Count only applies when the background is a video file."
                ),
            },
        ),
        (
            _("Login Page — Layout"),
            {
                "fields": (
                    "login_layout",
                    "login_split_show_overlay_text",
                    "login_split_overlay_text",
                    "login_split_text_position",
                ),
                "description": _(
                    "Choose the page structure. The split-screen options divide the page into a "
                    "full-bleed background panel and a dark login panel — use the fields below to "
                    "control the text shown on the background side."
                ),
            },
        ),
        (
            _("Login Page — Branding"),
            {
                "fields": (
                    "login_logo_url",
                    "login_logo_library",
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
            _("Login Page — Custom Code"),
            {
                "fields": ("login_page_css_url", "login_page_css", "login_page_head_html", "login_page_body_html"),
                "description": _(
                    "CSS and HTML injected exclusively on the login page, after all global styles. "
                    "Use these to fully restyle the login experience without affecting the rest of the site. "
                    "HTML fields are not sanitized — admin use only."
                ),
            },
        ),
        (
            _("Favicon"),
            {
                "fields": ("favicon_url", "favicon_library", "favicon"),
                "description": _(
                    "Replace the Alliance Auth favicon. URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Navigation Bar Logo"),
            {
                "fields": ("navbar_logo_url", "navbar_logo_library", "navbar_logo", "navbar_logo_height"),
                "description": _(
                    "Optional logo displayed next to the site name in the navbar. "
                    "URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Sidebar Logo"),
            {
                "fields": ("sidebar_logo_url", "sidebar_logo_library", "sidebar_logo", "sidebar_logo_width"),
                "description": _(
                    "Replaces the Alliance Auth logo at the bottom of the sidebar. "
                    "URL takes priority over an uploaded file."
                ),
            },
        ),
        (
            _("Site-Wide CSS & HTML"),
            {
                "fields": ("custom_css_url", "custom_css", "head_extra_html"),
                "description": _(
                    "Inject CSS and HTML into every page of the site. "
                    "The URL stylesheet is loaded first, then inline CSS — both after the active AA theme. "
                    "Works alongside Alliance Auth's built-in Custom CSS admin. "
                    "The &lt;head&gt; HTML field is not sanitized — admin use only."
                ),
            },
        ),
        (
            _("Main Dashboard — Custom Code"),
            {
                "fields": ("dashboard_css_url", "dashboard_css", "dashboard_head_html", "dashboard_body_html"),
                "description": _(
                    "CSS and HTML injected exclusively on the main dashboard page, after all global styles. "
                    "Use these to style or extend the dashboard widgets without affecting the rest of the site. "
                    "HTML fields are not sanitized — admin use only."
                ),
            },
        ),
        (
            _("Admin Dashboard — Custom Code"),
            {
                "fields": ("superuser_dashboard_css_url", "superuser_dashboard_css", "superuser_dashboard_head_html", "superuser_dashboard_body_html"),
                "description": _(
                    "CSS and HTML injected exclusively inside the admin status widget, visible to superusers only. "
                    "Non-superusers never receive these styles or markup. "
                    "HTML fields are not sanitized — admin use only."
                ),
            },
        ),
    )
