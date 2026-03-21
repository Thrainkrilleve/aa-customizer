from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_customizer", "0004_merge_20260321_0059"),
    ]

    operations = [
        migrations.AddField(
            model_name="custombranding",
            name="sidebar_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="aa_customizer/logos/",
                verbose_name="Sidebar Logo — Upload",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="sidebar_logo_url",
            field=models.URLField(blank=True, verbose_name="Sidebar Logo — URL"),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="sidebar_logo_width",
            field=models.PositiveSmallIntegerField(
                default=128, verbose_name="Sidebar Logo Width (px)"
            ),
        ),
    ]
