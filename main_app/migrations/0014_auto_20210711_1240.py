# Generated by Django 3.1.6 on 2021-07-11 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_auto_20210711_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Price'),
        ),
    ]
