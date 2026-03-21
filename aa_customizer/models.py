"""
Models for the aa_customizer app.
"""

from solo.models import SingletonModel

from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomBranding(SingletonModel):
    """
    Singleton model for Alliance Auth branding customization.

    Every visual element has a companion URL field.  The URL takes priority over
    an uploaded file so that Docker administrators can point to external images
    (e.g. a CDN, Imgur, or object storage) without needing a mounted media volume.

    Priority order for each image: URL field → uploaded file → AA default.
    """

    # ------------------------------------------------------------------ site --
    site_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Site Name"),
        help_text=_(
            "Override the site name shown in the browser title, navbar, and login "
            "page. Leave blank to use the value from your local.py settings."
        ),
    )

    # ----------------------------------------------- login background image --
    login_background = models.ImageField(
        upload_to="aa_customizer/backgrounds/",
        blank=True,
        null=True,
        verbose_name=_("Login Background — Upload"),
        help_text=_(
            "Upload a background image for the login page. "
            "Recommended: at least 1920×1080 px, JPEG or PNG. "
            "Ignored when a URL is also provided."
        ),
    )
    login_background_url = models.URLField(
        blank=True,
        verbose_name=_("Login Background — URL"),
        help_text=_(
            "URL of a background image (e.g. a CDN, Imgur, or object-storage link). "
            "Takes priority over an uploaded file. Ideal for Docker installs."
        ),
    )
    login_background_color = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("Login Background Color"),
        help_text=_(
            "Fallback CSS background color used when neither an image URL nor an "
            "uploaded file is set (e.g. #1a1a2e or rgba(26,26,46,1))."
        ),
    )

    # ---------------------------------------------------- login card logo -----
    login_logo = models.ImageField(
        upload_to="aa_customizer/logos/",
        blank=True,
        null=True,
        verbose_name=_("Login Logo — Upload"),
        help_text=_(
            "Upload a logo to display at the top of the login card. "
            "Recommended: transparent PNG, at least 256×256 px. "
            "Ignored when a URL is also provided."
        ),
    )
    login_logo_url = models.URLField(
        blank=True,
        verbose_name=_("Login Logo — URL"),
        help_text=_("URL of a logo image. Takes priority over an uploaded file."),
    )
    login_logo_max_width = models.PositiveSmallIntegerField(
        default=200,
        verbose_name=_("Login Logo Max Width (px)"),
        help_text=_("Maximum display width of the login logo in pixels."),
    )
    login_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Login Page Title"),
        help_text=_("Custom heading shown on the login card above the SSO button."),
    )
    login_subtitle = models.TextField(
        blank=True,
        verbose_name=_("Login Page Subtitle"),
        help_text=_("Optional description text shown below the title."),
    )
    login_extra_html = models.TextField(
        blank=True,
        verbose_name=_("Login Page Extra HTML"),
        help_text=_(
            "Raw HTML injected below the EVE SSO button on the login card. "
            "Useful for custom notices, Discord invite buttons, or extra links. "
            "Only editable by admins — content is rendered without sanitization."
        ),
    )

    # ---------------------------------------------------------- login layout --
    LAYOUT_CARD = "card"
    LAYOUT_SPLIT = "split"
    LAYOUT_SPLIT_RIGHT = "split-right"
    LAYOUT_CHOICES = [
        (LAYOUT_CARD, _("Centered Card (default)")),
        (LAYOUT_SPLIT, _("Split Screen — Background Left, Login Right")),
        (LAYOUT_SPLIT_RIGHT, _("Split Screen — Login Left, Background Right")),
    ]
    login_layout = models.CharField(
        max_length=15,
        choices=LAYOUT_CHOICES,
        default=LAYOUT_CARD,
        verbose_name=_("Login Page Layout"),
        help_text=_(
            "Centered Card: login card centered over a full-page background. "
            "Split Screen: divides the page into a background panel and a dark login panel — "
            "choose which side each appears on."
        ),
    )

    SPLIT_TEXT_TOP = "top"
    SPLIT_TEXT_CENTER = "center"
    SPLIT_TEXT_BOTTOM = "bottom"
    SPLIT_TEXT_CHOICES = [
        (SPLIT_TEXT_TOP, _("Top")),
        (SPLIT_TEXT_CENTER, _("Center")),
        (SPLIT_TEXT_BOTTOM, _("Bottom")),
    ]
    login_split_overlay_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Split Panel — Overlay Text"),
        help_text=_(
            "Text shown on the background panel in split layouts. "
            "Leave blank to display the site name automatically."
        ),
    )
    login_split_show_overlay_text = models.BooleanField(
        default=True,
        verbose_name=_("Split Panel — Show Overlay Text"),
        help_text=_(
            "Tick to display text on the background panel; untick to hide it entirely."
        ),
    )
    login_split_text_position = models.CharField(
        max_length=10,
        choices=SPLIT_TEXT_CHOICES,
        default=SPLIT_TEXT_CENTER,
        verbose_name=_("Split Panel — Text Position"),
        help_text=_("Vertical position of the overlay text on the background panel."),
    )

    # ---------------------------------------------------------------- favicon --
    favicon = models.ImageField(
        upload_to="aa_customizer/icons/",
        blank=True,
        null=True,
        verbose_name=_("Favicon — Upload"),
        help_text=_(
            "Upload a custom favicon. "
            "Recommended: PNG or ICO, at least 192×192 px. "
            "Ignored when a URL is also provided."
        ),
    )
    favicon_url = models.URLField(
        blank=True,
        verbose_name=_("Favicon — URL"),
        help_text=_("URL of a favicon image. Takes priority over an uploaded file."),
    )

    # ---------------------------------------------------------- navbar logo ---
    navbar_logo = models.ImageField(
        upload_to="aa_customizer/logos/",
        blank=True,
        null=True,
        verbose_name=_("Navbar Logo — Upload"),
        help_text=_(
            "Upload a logo for the top navigation bar. "
            "Recommended: transparent PNG. "
            "Ignored when a URL is also provided."
        ),
    )
    navbar_logo_url = models.URLField(
        blank=True,
        verbose_name=_("Navbar Logo — URL"),
        help_text=_("URL of a navbar logo image. Takes priority over an uploaded file."),
    )
    navbar_logo_height = models.PositiveSmallIntegerField(
        default=32,
        verbose_name=_("Navbar Logo Height (px)"),
        help_text=_("Display height of the navbar logo in pixels."),
    )

    # --------------------------------------------------------- sidebar logo ---
    sidebar_logo = models.ImageField(
        upload_to="aa_customizer/logos/",
        blank=True,
        null=True,
        verbose_name=_("Sidebar Logo — Upload"),
        help_text=_(
            "Upload a logo to replace the Alliance Auth logo in the sidebar. "
            "Recommended: transparent PNG. "
            "Ignored when a URL is also provided."
        ),
    )
    sidebar_logo_url = models.URLField(
        blank=True,
        verbose_name=_("Sidebar Logo — URL"),
        help_text=_("URL of a sidebar logo image. Takes priority over an uploaded file."),
    )
    sidebar_logo_width = models.PositiveSmallIntegerField(
        default=128,
        verbose_name=_("Sidebar Logo Width (px)"),
        help_text=_("Display width of the sidebar logo in pixels."),
    )

    # -------------------------------------------------------------- custom CSS --
    custom_css = models.TextField(
        blank=True,
        verbose_name=_("Custom CSS"),
        help_text=_(
            "CSS injected into every page via an inline <style> block, loaded after "
            "the active theme so it can override any style. "
            "Works alongside Alliance Auth's built-in Custom CSS admin."
        ),
    )
    custom_css_url = models.URLField(
        blank=True,
        verbose_name=_("Custom CSS — URL"),
        help_text=_(
            "URL of an external CSS stylesheet linked in every page <head> "
            "(e.g. a CDN-hosted custom theme file). Loaded after the active AA theme."
        ),
    )

    # ------------------------------------------------------------ extra HTML --
    head_extra_html = models.TextField(
        blank=True,
        verbose_name=_("Extra <head> HTML"),
        help_text=_(
            "Raw HTML injected at the very end of <head> on every page. "
            "Useful for analytics scripts, font imports, or custom meta tags. "
            "Only editable by admins — content is rendered without sanitization."
        ),
    )

    class Meta:
        default_permissions = ("view", "change")
        verbose_name = _("Custom Branding")
        verbose_name_plural = _("Custom Branding")

    def __str__(self) -> str:
        return str(_("Custom Branding"))

    # ---------------------------------------------------------------- helpers --

    @property
    def effective_login_background(self) -> str:
        """URL field > uploaded file > empty string."""
        if self.login_background_url:
            return self.login_background_url
        if self.login_background:
            return self.login_background.url
        return ""

    _VIDEO_EXTENSIONS = (".mp4", ".webm", ".ogv", ".ogg")

    @property
    def effective_login_background_is_video(self) -> bool:
        """Return True when the effective login background is a video file."""
        url = self.effective_login_background
        if not url:
            return False
        # Strip query-string / fragment before checking extension
        path = url.split("?")[0].split("#")[0].lower()
        return any(path.endswith(ext) for ext in self._VIDEO_EXTENSIONS)

    @property
    def effective_login_logo(self) -> str:
        """URL field > uploaded file > empty string."""
        if self.login_logo_url:
            return self.login_logo_url
        if self.login_logo:
            return self.login_logo.url
        return ""

    @property
    def effective_favicon(self) -> str:
        """URL field > uploaded file > empty string."""
        if self.favicon_url:
            return self.favicon_url
        if self.favicon:
            return self.favicon.url
        return ""

    @property
    def effective_navbar_logo(self) -> str:
        """URL field > uploaded file > empty string."""
        if self.navbar_logo_url:
            return self.navbar_logo_url
        if self.navbar_logo:
            return self.navbar_logo.url
        return ""

    @property
    def effective_sidebar_logo(self) -> str:
        """URL field > uploaded file > empty string."""
        if self.sidebar_logo_url:
            return self.sidebar_logo_url
        if self.sidebar_logo:
            return self.sidebar_logo.url
        return ""
