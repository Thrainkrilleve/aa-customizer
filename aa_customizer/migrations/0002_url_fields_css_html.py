from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_customizer", "0001_initial"),
    ]

    operations = [
        # ── URL companions for image fields ────────────────────────────────
        migrations.AddField(
            model_name="custombranding",
            name="login_background_url",
            field=models.URLField(
                blank=True,
                verbose_name="Login Background — URL",
                help_text=(
                    "URL of a background image (e.g. a CDN, Imgur, or object-storage link). "
                    "Takes priority over an uploaded file. Ideal for Docker installs."
                ),
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_logo_url",
            field=models.URLField(
                blank=True,
                verbose_name="Login Logo — URL",
                help_text="URL of a logo image. Takes priority over an uploaded file.",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="favicon_url",
            field=models.URLField(
                blank=True,
                verbose_name="Favicon — URL",
                help_text="URL of a favicon image. Takes priority over an uploaded file.",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="navbar_logo_url",
            field=models.URLField(
                blank=True,
                verbose_name="Navbar Logo — URL",
                help_text="URL of a navbar logo image. Takes priority over an uploaded file.",
            ),
        ),
        # ── Rename verbose names on existing image fields to "— Upload" ───
        migrations.AlterField(
            model_name="custombranding",
            name="login_background",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="aa_customizer/backgrounds/",
                verbose_name="Login Background — Upload",
                help_text=(
                    "Upload a background image for the login page. "
                    "Ignored when a URL is also provided."
                ),
            ),
        ),
        migrations.AlterField(
            model_name="custombranding",
            name="login_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="aa_customizer/logos/",
                verbose_name="Login Logo — Upload",
                help_text=(
                    "Upload a logo to display at the top of the login card. "
                    "Ignored when a URL is also provided."
                ),
            ),
        ),
        migrations.AlterField(
            model_name="custombranding",
            name="favicon",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="aa_customizer/icons/",
                verbose_name="Favicon — Upload",
                help_text="Upload a custom favicon. Ignored when a URL is also provided.",
            ),
        ),
        migrations.AlterField(
            model_name="custombranding",
            name="navbar_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="aa_customizer/logos/",
                verbose_name="Navbar Logo — Upload",
                help_text=(
                    "Upload a logo for the top navigation bar. "
                    "Ignored when a URL is also provided."
                ),
            ),
        ),
        # ── Custom CSS ────────────────────────────────────────────────────
        migrations.AddField(
            model_name="custombranding",
            name="custom_css",
            field=models.TextField(
                blank=True,
                verbose_name="Custom CSS",
                help_text=(
                    "CSS injected into every page via an inline <style> block, "
                    "loaded after the active theme."
                ),
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="custom_css_url",
            field=models.URLField(
                blank=True,
                verbose_name="Custom CSS — URL",
                help_text=(
                    "URL of an external CSS stylesheet linked in every page <head>. "
                    "Loaded after the active AA theme."
                ),
            ),
        ),
        # ── Login extra HTML ──────────────────────────────────────────────
        migrations.AddField(
            model_name="custombranding",
            name="login_extra_html",
            field=models.TextField(
                blank=True,
                verbose_name="Login Page Extra HTML",
                help_text=(
                    "Raw HTML injected below the EVE SSO button on the login card. "
                    "Only editable by admins — content is rendered without sanitization."
                ),
            ),
        ),
        # ── Extra <head> HTML ─────────────────────────────────────────────
        migrations.AddField(
            model_name="custombranding",
            name="head_extra_html",
            field=models.TextField(
                blank=True,
                verbose_name="Extra <head> HTML",
                help_text=(
                    "Raw HTML injected at the very end of <head> on every page. "
                    "Only editable by admins — content is rendered without sanitization."
                ),
            ),
        ),
    ]
