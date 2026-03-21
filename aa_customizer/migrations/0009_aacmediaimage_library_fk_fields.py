"""
Migration: add AACMediaImage media library model and library FK fields
on CustomBranding for each image slot.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_customizer", "0008_alter_custombranding_login_layout_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AACMediaImage",
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
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "image",
                    models.ImageField(
                        upload_to="aa_customizer/library/", verbose_name="Image"
                    ),
                ),
                (
                    "image_type",
                    models.CharField(
                        choices=[
                            ("any", "Any / General"),
                            ("background", "Background"),
                            ("logo", "Logo"),
                            ("icon", "Icon / Favicon"),
                        ],
                        default="any",
                        max_length=20,
                        verbose_name="Type",
                    ),
                ),
                (
                    "uploaded",
                    models.DateTimeField(auto_now_add=True, verbose_name="Uploaded"),
                ),
            ],
            options={
                "verbose_name": "Media Library Image",
                "verbose_name_plural": "Media Library",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_background_library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="aa_customizer.aacmediaimage",
                verbose_name="Login Background — Library",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="login_logo_library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="aa_customizer.aacmediaimage",
                verbose_name="Login Logo — Library",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="favicon_library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="aa_customizer.aacmediaimage",
                verbose_name="Favicon — Library",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="navbar_logo_library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="aa_customizer.aacmediaimage",
                verbose_name="Navbar Logo — Library",
            ),
        ),
        migrations.AddField(
            model_name="custombranding",
            name="sidebar_logo_library",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="aa_customizer.aacmediaimage",
                verbose_name="Sidebar Logo — Library",
            ),
        ),
    ]
