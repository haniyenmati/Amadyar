# Generated by Django 3.2.12 on 2022-04-10 04:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('haul', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimationFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.FileField(upload_to='')),
                ('routes', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='estimation_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 4, 59, 19, 731783)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='estimation_start',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 4, 59, 44, 118540)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderlog',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='orderlog',
            name='longtitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='storage',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='storage',
            name='longtitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='store',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='store',
            name='longtitude',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='PathEstimation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longtitude', models.FloatField(default=0)),
                ('latitude', models.FloatField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Paths', to='haul.order')),
            ],
        ),
    ]
