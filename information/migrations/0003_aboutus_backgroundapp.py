# Generated by Django 5.0.4 on 2024-04-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0002_rename_back_aboutus_backgroundimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='backgroundApp',
            field=models.ImageField(blank=True, null=True, upload_to='Back_logo/'),
        ),
    ]