# Generated by Django 4.1.7 on 2023-05-05 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recapp', '0002_delete_recette'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image_url', models.CharField(max_length=200)),
            ],
        ),
    ]
