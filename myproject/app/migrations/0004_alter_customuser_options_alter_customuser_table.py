# Generated by Django 5.1.3 on 2024-11-11 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customuser_date_joined_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='test_user',
        ),
    ]