from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_customizer", "0005_custombranding_sidebar_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="custombranding",
            name="login_layout",
            field=models.CharField(
                choices=[("card", "Centered Card (default)"), ("split", "Split Screen")],
                default="card",
                max_length=10,
                verbose_name="Login Page Layout",
            ),
        ),
    ]
