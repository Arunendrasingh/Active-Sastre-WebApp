# Generated by Django 3.1.6 on 2021-07-10 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_auto_20210710_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='p_Hips',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
