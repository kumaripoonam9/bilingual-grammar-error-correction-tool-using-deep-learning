# Generated by Django 4.1.3 on 2023-02-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0004_remove_expertlanguage_languages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertlanguage',
            name='languages_known',
            field=models.CharField(choices=[('Hindi', 'Hindi'), ('English', 'English'), ('Both hindi and english', 'Both hindi and english')], max_length=255),
        ),
    ]
