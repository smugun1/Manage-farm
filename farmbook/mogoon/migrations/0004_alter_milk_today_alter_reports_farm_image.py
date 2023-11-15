# Generated by Django 4.2.3 on 2023-11-15 15:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogoon', '0003_remove_reports_image_reports_farm_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milk',
            name='today',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 15, 18, 5, 44, 370382)),
        ),
        migrations.AlterField(
            model_name='reports',
            name='farm_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]