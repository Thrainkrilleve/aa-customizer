"""
Models for the aa_customizer app.
"""

import os

from solo.models import SingletonModel

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

_ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg"}
_ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogv", ".ogg"}
_ALLOWED_BACKGROUND_EXTENSIONS = _ALLOWED_IMAGE_EXTENSIONS | _ALLOWED_VIDEO_EXTENSIONS


def validate_image_or_video(value):
    """Accept standard image formats and web video formats (.mp4, .webm, .ogv)."""
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in _ALLOWED_BACKGROUND_EXTENSIONS:
        raise ValidationError(
            "Unsupported file type '%(ext)s'. "
            "Allowed images: %(images)s. "
            "Allowed videos: %(videos)s.",
            params={
                "ext": ext,
                "images": ", ".join(sorted(_ALLOWED_IMAGE_EXTENSIONS)),
                "videos": ", ".join(sorted(_ALLOWED_VIDEO_EXTENSIONS)),
            },
        )


class AACMediaImage(models.Model):
    """
    Media library image.  Upload images here once, then select them from any
    image field in Custom Branding — no need to re-upload or copy files.
    """

    IMAGE_TYPE_ANY = "any"
    IMAGE_TYPE_BACKGROUND = "background"
    IMAGE_TYPE_LOGO = "logo"
    IMAGE_TYPE_ICON = "icon"
    IMAGE_TYPE_CHOICES = [
        (IMAGE_TYPE_ANY, _("Any / General")),
        (IMAGE_TYPE_BACKGROUND, _("Background")),
        (IMAGE_TYPE_LOGO, _("Logo")),
        (IMAGE_TYPE_ICON, _("Icon / Favicon")),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_(
            "A descriptive label for this image, e.g. 'Corp logo v2' or 'Winter background'."
        ),
    )
    image = models.ImageField(
        upload_to="aa_customizer/library/",
        verbose_name=_("Image"),
    )
    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE_CHOICES,
        default=IMAGE_TYPE_ANY,
        verbose_name=_("Type"),
        help_text=_("Optional category for organisation — does not restrict usage."),
    )
    uploaded = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded"))

    class Meta:
        verbose_name = _("Media Library Image")
        verbose_name_plural = _("Media Library")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


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
    login_background = models.FileField(
        upload_to="aa_customizer/backgrounds/",
        blank=True,
        null=True,
        validators=[validate_image_or_video],
        verbose_name=_("Login Background — Upload"),
        help_text=_(
            "Upload a background image or video for the login page. "
            "Images: JPEG, PNG, GIF, WebP (recommended: at least 1920×1080 px). "
            "Videos: MP4, WebM, OGV. "
            "Ignored when a URL is also provided."
        ),
    )
    login_background_url = models.URLField(
        blank=True,
        verbose_name=_("Login Background — URL"),
        help_text=_(
            "URL of a background image or video file (e.g. a CDN, Imgur, or object-storage link). "
            "Takes priority over an uploaded file. Ideal for Docker installs. "
            "Supported video formats: .mp4, .webm, .ogv. "
            "Note: YouTube and other streaming links are not supported — the URL must point directly to a file."
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
    login_background_library = models.ForeignKey(
        "AACMediaImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Login Background — Library"),
        help_text=_(
            "Select an image from the media library. "
            "Takes priority over a direct upload; a URL takes priority over both."
        ),
    )
    login_background_video_loop_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Background Video — Loop Count"),
        help_text=_(
            "How many times to play the background video before stopping. "
            "0 = loop forever (default). "
            "1 = play once then freeze on the last frame. "
            "2, 3, … = play that many times then freeze. "
            "Has no effect when the background is a static image."
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
    login_logo_library = models.ForeignKey(
        "AACMediaImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Login Logo — Library"),
        help_text=_(
            "Select an image from the media library. "
            "Takes priority over a direct upload; a URL takes priority over both."
        ),
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
    favicon_library = models.ForeignKey(
        "AACMediaImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Favicon — Library"),
        help_text=_(
            "Select an image from the media library. "
            "Takes priority over a direct upload; a URL takes priority over both."
        ),
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
    navbar_logo_library = models.ForeignKey(
        "AACMediaImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Navbar Logo — Library"),
        help_text=_(
            "Select an image from the media library. "
            "Takes priority over a direct upload; a URL takes priority over both."
        ),
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
    sidebar_logo_library = models.ForeignKey(
        "AACMediaImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Sidebar Logo — Library"),
        help_text=_(
            "Select an image from the media library. "
            "Takes priority over a direct upload; a URL takes priority over both."
        ),
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
            "Inline &lt;style&gt; block applied to every page, after the URL stylesheet and active theme."
        ),
    )
    custom_css_url = models.URLField(
        blank=True,
        verbose_name=_("Custom CSS — URL"),
        help_text=_(
            "URL of an external stylesheet linked in &lt;head&gt; on every page "
            "(e.g. a CDN-hosted theme or Google Fonts)."
        ),
    )

    # ------------------------------------------------------------ extra HTML --
    head_extra_html = models.TextField(
        blank=True,
        verbose_name=_("Extra &lt;head&gt; HTML"),
        help_text=_(
            "Raw HTML injected at the end of &lt;head&gt; on every page "
            "(analytics scripts, font imports, meta tags). Not sanitized."
        ),
    )

    # ------------------------------------------ login page — custom code -----
    login_page_css_url = models.URLField(
        blank=True,
        verbose_name=_("Login Page — CSS URL"),
        help_text=_(
            "External stylesheet URL loaded on the login page after the global CSS URL. "
            "Use this to pull in a separate design framework (e.g. Tailwind CDN) "
            "without affecting the rest of the site."
        ),
    )
    login_page_css = models.TextField(
        blank=True,
        verbose_name=_("Login Page — CSS"),
        help_text=_(
            "Inline CSS applied last on the login page, after all other stylesheets — "
            "highest priority, full design control over the card layout, colors, and fonts."
        ),
    )
    login_page_head_html = models.TextField(
        blank=True,
        verbose_name=_("Login Page — Extra &lt;head&gt; HTML"),
        help_text=_(
            "Raw HTML injected at the end of &lt;head&gt; on the login page "
            "(custom fonts, icon libraries, JS frameworks, Open Graph tags). Not sanitized."
        ),
    )
    login_page_body_html = models.TextField(
        blank=True,
        verbose_name=_("Login Page — Extra Body HTML"),
        help_text=_(
            "Raw HTML injected before &lt;/body&gt; on the login page "
            "(overlays, animation scripts, custom markup). Not sanitized."
        ),
    )

    class Meta:  # type: ignore[override]
        default_permissions = ("view", "change")
        verbose_name = _("Custom Branding")
        verbose_name_plural = _("Custom Branding")

    def __str__(self) -> str:
        return str(_("Custom Branding"))

    # ---------------------------------------------------------------- helpers --

    @property
    def effective_login_background(self) -> str:
        """URL field > library selection > uploaded file > empty string."""
        if self.login_background_url:
            return self.login_background_url
        lib = self.login_background_library
        if lib is not None and lib.image:
            return lib.image.url
        if self.login_background:
            return self.login_background.url
        return ""

    _VIDEO_EXTENSIONS = (".mp4", ".webm", ".ogv", ".ogg")
    _VIDEO_MIME_TYPES = {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".ogv": "video/ogg",
        ".ogg": "video/ogg",
    }

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
    def effective_login_background_mime_type(self) -> str:
        """Return the MIME type for the effective login background video."""
        url = self.effective_login_background
        if not url:
            return ""
        path = url.split("?")[0].split("#")[0].lower()
        for ext, mime in self._VIDEO_MIME_TYPES.items():
            if path.endswith(ext):
                return mime
        return ""

    @property
    def effective_login_logo(self) -> str:
        """URL field > library selection > uploaded file > empty string."""
        if self.login_logo_url:
            return self.login_logo_url
        lib = self.login_logo_library
        if lib is not None and lib.image:
            return lib.image.url
        if self.login_logo:
            return self.login_logo.url
        return ""

    @property
    def effective_favicon(self) -> str:
        """URL field > library selection > uploaded file > empty string."""
        if self.favicon_url:
            return self.favicon_url
        lib = self.favicon_library
        if lib is not None and lib.image:
            return lib.image.url
        if self.favicon:
            return self.favicon.url
        return ""

    @property
    def effective_navbar_logo(self) -> str:
        """URL field > library selection > uploaded file > empty string."""
        if self.navbar_logo_url:
            return self.navbar_logo_url
        lib = self.navbar_logo_library
        if lib is not None and lib.image:
            return lib.image.url
        if self.navbar_logo:
            return self.navbar_logo.url
        return ""

    @property
    def effective_sidebar_logo(self) -> str:
        """URL field > library selection > uploaded file > empty string."""
        if self.sidebar_logo_url:
            return self.sidebar_logo_url
        lib = self.sidebar_logo_library
        if lib is not None and lib.image:
            return lib.image.url
        if self.sidebar_logo:
            return self.sidebar_logo.url
        return ""
