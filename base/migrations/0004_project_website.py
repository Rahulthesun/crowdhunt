# Generated by Django 4.2.18 on 2025-02-01 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_project_projectpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
