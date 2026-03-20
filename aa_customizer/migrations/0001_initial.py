# Generated migration for aa_customizer

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomBranding",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "site_name",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Override the site name displayed in the browser title, "
                            "navbar, and login page. Leave blank to use the value "
                            "from your local.py settings."
                        ),
                        max_length=100,
                        verbose_name="Site Name",
                    ),
                ),
                (
                    "login_background",
                    models.ImageField(
                        blank=True,
                        help_text=(
                            "Custom background image for the login page. "
                            "Recommended: at least 1920x1080 px, JPEG or PNG."
                        ),
                        null=True,
                        upload_to="aa_customizer/backgrounds/",
                        verbose_name="Login Background Image",
                    ),
                ),
                (
                    "login_background_color",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Fallback background color for the login page when no "
                            "background image is set (e.g. #1a1a2e). "
                            "Ignored when a background image is provided."
                        ),
                        max_length=30,
                        verbose_name="Login Background Color",
                    ),
                ),
                (
                    "login_logo",
                    models.ImageField(
                        blank=True,
                        help_text=(
                            "Logo displayed at the top of the login card. "
                            "Recommended: transparent PNG, at least 256x256 px."
                        ),
                        null=True,
                        upload_to="aa_customizer/logos/",
                        verbose_name="Login Page Logo",
                    ),
                ),
                (
                    "login_logo_max_width",
                    models.PositiveSmallIntegerField(
                        default=200,
                        help_text="Maximum width of the login logo in pixels.",
                        verbose_name="Login Logo Max Width (px)",
                    ),
                ),
                (
                    "login_title",
                    models.CharField(
                        blank=True,
                        help_text="Custom title / welcome heading shown on the login card.",
                        max_length=200,
                        verbose_name="Login Page Title",
                    ),
                ),
                (
                    "login_subtitle",
                    models.TextField(
                        blank=True,
                        help_text=(
                            "Optional description text shown below the title "
                            "on the login card."
                        ),
                        verbose_name="Login Page Subtitle",
                    ),
                ),
                (
                    "favicon",
                    models.ImageField(
                        blank=True,
                        help_text=(
                            "Custom site favicon used in browser tabs, bookmarks, "
                            "and the navbar. Recommended: PNG or ICO, at least 192x192 px."
                        ),
                        null=True,
                        upload_to="aa_customizer/icons/",
                        verbose_name="Favicon",
                    ),
                ),
                (
                    "navbar_logo",
                    models.ImageField(
                        blank=True,
                        help_text=(
                            "Logo displayed in the top-left navigation bar. "
                            "Recommended: transparent PNG."
                        ),
                        null=True,
                        upload_to="aa_customizer/logos/",
                        verbose_name="Navbar Logo",
                    ),
                ),
                (
                    "navbar_logo_height",
                    models.PositiveSmallIntegerField(
                        default=32,
                        help_text="Display height of the navbar logo in pixels.",
                        verbose_name="Navbar Logo Height (px)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Custom Branding",
                "verbose_name_plural": "Custom Branding",
                "default_permissions": (),
            },
        ),
    ]
