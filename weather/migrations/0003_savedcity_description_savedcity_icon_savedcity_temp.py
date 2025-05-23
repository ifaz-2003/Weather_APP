# Generated by Django 5.1.1 on 2025-03-03 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0002_savedcity"),
    ]

    operations = [
        migrations.AddField(
            model_name="savedcity",
            name="description",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="savedcity",
            name="icon",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="savedcity",
            name="temp",
            field=models.FloatField(default=0.0),
        ),
    ]
