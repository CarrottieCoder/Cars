# Generated by Django 4.2.13 on 2024-07-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_carmake_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmake',
            name='other_data',
            field=models.TextField(blank=True, default=''),
        ),
    ]