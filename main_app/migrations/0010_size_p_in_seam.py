# Generated by Django 3.1.6 on 2021-07-10 05:00

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='p_In_Seam',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Price'),
            preserve_default=False,
        ),
    ]
