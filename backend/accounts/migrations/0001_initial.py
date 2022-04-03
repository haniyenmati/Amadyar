# Generated by Django 3.2.12 on 2022-04-03 13:43

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=256)),
                ('last_name', models.CharField(blank=True, default='', max_length=256)),
                ('national_code', models.CharField(max_length=16, unique=True)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('otp', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
