# Generated by Django 4.2.18 on 2025-02-01 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_project_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpost',
            name='poster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.hunterprofile'),
        ),
    ]
