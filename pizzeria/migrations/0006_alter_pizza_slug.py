# Generated by Django 4.2.2 on 2023-10-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0005_alter_pizza_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
