# Generated by Django 5.0.4 on 2024-04-24 14:32

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo/')),
                ('back', models.ImageField(blank=True, null=True, upload_to='Back_logo/')),
                ('about', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('born_date', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('github', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'about us ',
                'verbose_name_plural': 'about us ',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('from_email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=9)),
                ('message', models.TextField(verbose_name='Conteúdo')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Client contact',
                'verbose_name_plural': 'Client contacts',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='', max_length=3000, upload_to='carousel_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='chef/')),
                ('github', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Squad',
                'verbose_name_plural': 'Squad',
            },
        ),
        migrations.CreateModel(
            name='Why_Choose_Us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'why choose us ',
                'verbose_name_plural': 'why choose us ',
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('sub_title', models.CharField(max_length=100)),
                ('image', models.ManyToManyField(to='information.image')),
            ],
        ),
    ]
