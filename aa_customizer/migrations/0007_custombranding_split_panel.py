from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_customizer", "0006_custombranding_login_layout"),
    ]

    operations = [
        migrations.AlterField(
            model_name="custombranding",
            name="login_layout",
            field=models.CharField(
                choices=[
                    ("card", "Centered Card (default)"),
                    ("split", "Split Screen — Background Left, Login Right"),
                    ("split-right", "Split Screen — Login Left, Background Right"),
                ],
                default="card",
                max_length=15,
                verbose_name="Login Page Layout",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_split_overlay_text",
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name="Split Panel — Overlay Text",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_split_show_overlay_text",
            field=models.BooleanField(
                default=True,
                verbose_name="Split Panel — Show Overlay Text",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_split_text_position",
            field=models.CharField(
                choices=[("top", "Top"), ("center", "Center"), ("bottom", "Bottom")],
                default="center",
                max_length=10,
                verbose_name="Split Panel — Text Position",
            ),
        ),
    ]
