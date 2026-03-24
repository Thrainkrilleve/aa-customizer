"""
Admin configuration for the aa_customizer app.
Organized into collapsible sections to separate basic branding from advanced code.
"""

from solo.admin import SingletonModelAdmin

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import CustomBrandingAdminForm
from .models import AACMediaImage, CustomBranding
from .permissions import _is_trusted_admin


@admin.register(AACMediaImage)
class AACMediaImageAdmin(admin.ModelAdmin):
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
    form = CustomBrandingAdminForm
    save_on_top = True

    def has_view_permission(self, request, obj=None):
        return _is_trusted_admin(request)

    def has_change_permission(self, request, obj=None):
        return _is_trusted_admin(request)

    def has_add_permission(self, request):
        return False  # singleton — cannot add

    def has_delete_permission(self, request, obj=None):
        return False  # singleton — cannot delete

    # Organized fieldsets to act like sections/tabs
    fieldsets = (
        (
            _("Basic Branding"),
            {
                "fields": (
                    "site_name",
                    "favicon_url", "favicon_library", "favicon",
                    "navbar_logo_url", "navbar_logo_library", "navbar_logo", "navbar_logo_height",
                    "sidebar_logo_url", "sidebar_logo_library", "sidebar_logo", "sidebar_logo_width",
                ),
                "description": _("General site-wide visual settings."),
            },
        ),
        (
            _("Login Page — Layout & Visuals"),
            {
                "fields": (
                    "login_layout",
                    "login_background_url", "login_background_library", "login_background", "login_background_color",
                    "login_background_video_loop_count",
                    "login_logo_url", "login_logo_library", "login_logo", "login_logo_max_width",
                    "login_title", "login_subtitle",
                    "login_split_show_overlay_text", "login_split_overlay_text", "login_split_text_position",
                ),
            },
        ),
        (
            _("Global Custom Code"),
            {
                "classes": ("collapse",),  # Collapsed by default to reduce clutter
                "fields": ("custom_css_url", "custom_css", "head_extra_html"),
                "description": _("CSS and HTML injected into every page on the site."),
            },
        ),
        (
            _("Login Page — SPA Mode"),
            {
                "classes": ("collapse",),
                "fields": (
                    "login_spa_enabled",
                    "login_spa_nav_brand",
                ),
                "description": _(
                    "Turn the login page into a multi-page public-facing SPA. "
                    "Enable the toggle, then add your page content via the "
                    "'Login Page — Custom Code' › 'Extra Body HTML' field using "
                    "<div id=\"aac-spa-content\" style=\"display:none\"> "
                    "containing <section data-route=\"slug\" data-label=\"Nav Label\"> elements. "
                    "A 'Sign In' link in the nav bar reveals the standard EVE SSO card. "
                    "Use the bundled CSS classes (aac-spa-page, aac-spa-hero-title, "
                    "aac-spa-btn-primary, etc.) or supply your own via 'Login Page CSS'."
                ),
            },
        ),
        (
            _("Login Page — Custom Code"),
            {
                "classes": ("collapse",),
                "fields": (
                    "login_page_css_url",
                    "login_page_css",
                    "login_page_head_html",
                    "login_page_body_html",
                    "login_extra_html",
                ),
                "description": _("Code specific only to the login page."),
            },
        ),
        (
            _("Main Dashboard — Custom Code"),
            {
                "classes": ("collapse",),
                "fields": (
                    "dashboard_css_url",
                    "dashboard_css",
                    "dashboard_head_html",
                    "dashboard_body_html"
                ),
            },
        ),
        (
            _("Admin Dashboard — Custom Code"),
            {
                "classes": ("collapse",),
                "fields": (
                    "superuser_dashboard_css_url",
                    "superuser_dashboard_css",
                    "superuser_dashboard_head_html",
                    "superuser_dashboard_body_html"
                ),
            },
        ),
    )
