from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_customizer", "0016_dashboard_and_superuser_dashboard_custom_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="custombranding",
            name="login_spa_enabled",
            field=models.BooleanField(
                default=False,
                verbose_name="Login Page — Enable SPA mode",
                help_text=(
                    "When enabled, a full-viewport overlay SPA is shown on the login page. "
                    "Visitors see a multi-page public site (Home, About, Apply, …) with a "
                    "nav bar; clicking 'Sign In' reveals the standard EVE SSO card underneath."
                ),
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_spa_nav_brand",
            field=models.CharField(
                max_length=120,
                blank=True,
                default="",
                verbose_name="Login Page — SPA nav brand",
                help_text=(
                    "Text shown in the top-left of the SPA navigation bar. "
                    "Defaults to the site name if left blank."
                ),
            ),
        ),
    ]
