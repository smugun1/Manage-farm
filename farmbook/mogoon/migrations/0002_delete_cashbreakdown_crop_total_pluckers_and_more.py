# Generated by Django 4.0.4 on 2022-11-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogoon', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CashBreakdown',
        ),
        migrations.AddField(
            model_name='crop',
            name='total_pluckers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crops_p',
            name='total_pluckers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
