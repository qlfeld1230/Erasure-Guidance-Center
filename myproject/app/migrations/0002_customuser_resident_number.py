# Generated by Django 3.2.25 on 2024-10-31 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='resident_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
