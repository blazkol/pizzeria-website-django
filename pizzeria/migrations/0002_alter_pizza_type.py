# Generated by Django 4.2.2 on 2023-10-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='type',
            field=models.CharField(default='Standard', max_length=50),
        ),
    ]