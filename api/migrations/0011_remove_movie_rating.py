# Generated by Django 5.1.4 on 2024-12-27 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_review_review_review_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rating',
        ),
    ]