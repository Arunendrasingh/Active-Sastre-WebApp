# Generated by Django 3.1.6 on 2021-07-20 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0046_user_feedback_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='oreder_detail',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
