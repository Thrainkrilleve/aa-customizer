from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aa_customizer', '0010_alter_fields_django6_compat'),
    ]

    operations = [
        migrations.AddField(
            model_name='custombranding',
            name='login_background_video_loop_count',
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text='How many times to play the background video before stopping. 0 = loop forever (default). 1 = play once then freeze on the last frame. 2, 3, … = play that many times then freeze. Has no effect when the background is a static image.',
                verbose_name='Background Video — Loop Count',
            ),
        ),
    ]
