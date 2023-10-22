# Generated by Django 4.2.2 on 2023-10-22 18:01

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0009_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField()),
                ('last_name', models.CharField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('city', models.CharField()),
                ('street', models.CharField()),
                ('house_number', models.IntegerField()),
                ('apartment_number', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField()),
            ],
        ),
        migrations.AlterField(
            model_name='pizza',
            name='ingredients',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='name',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='price_large',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='price_medium',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='city',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None),
        ),
    ]
