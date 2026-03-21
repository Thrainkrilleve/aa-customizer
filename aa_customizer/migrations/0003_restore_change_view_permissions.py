from django.db import migrations


class Migration(migrations.Migration):
    """
    Restore the 'change' and 'view' permissions for CustomBranding.

    The initial migration set default_permissions = () which prevented Django
    from creating *any* permissions for this model.  That means non-superuser
    staff users could never be granted change permission, so Django admin
    rendered the form without a Save button.

    Changing default_permissions to ("view", "change") causes Django's
    post_migrate signal to create those two permissions in auth_permission.
    """

    dependencies = [
        ("aa_customizer", "0002_url_fields_css_html"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="custombranding",
            options={
                "default_permissions": ("view", "change"),
                "verbose_name": "Custom Branding",
                "verbose_name_plural": "Custom Branding",
            },
        ),
    ]
