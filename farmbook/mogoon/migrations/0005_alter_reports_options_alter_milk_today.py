# Generated by Django 4.1.4 on 2023-05-11 03:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogoon', '0004_reports_alter_milk_today'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reports',
            options={'ordering': ('-time_stamp',)},
        ),
        migrations.AlterField(
            model_name='milk',
            name='today',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 5, 11, 6, 43, 29, 604133)),
        ),
    ]
