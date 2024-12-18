# Generated by Django 5.1.4 on 2024-12-14 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_movie_rating_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castandcrew',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cast_and_crew', to='api.movie'),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.movie'),
        ),
    ]
