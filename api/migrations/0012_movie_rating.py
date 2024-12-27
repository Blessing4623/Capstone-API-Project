# Generated by Django 5.1.4 on 2024-12-27 00:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_movie_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
    ]
