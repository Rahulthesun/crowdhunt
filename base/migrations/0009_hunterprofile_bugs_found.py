# Generated by Django 4.2.18 on 2025-02-01 22:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_projectpost_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunterprofile',
            name='bugs_found',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
